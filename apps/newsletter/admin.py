from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext, ugettext_lazy as _

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# This function is new in Django 1.2 - fallback to dummy identity
# function not to break compatibility with older releases.
try:
    from django.utils.formats import date_format
except ImportError:
    date_format = lambda value, format=None: value

from models import EmailTemplate, Newsletter, Subscription, Submission

from admin_forms import *
from admin_utils import *

class NewsletterAdmin(admin.ModelAdmin):

    change_form_template = 'newsletter/admin/add_newsletter.html'
    list_display = (
        'title',
        'admin_subscriptions',
        'admin_submissions',
    )
    prepopulated_fields = {
        'slug': ('title',)
    }
    filter_horizontal = [
        'photoreports',
        'newsitems',
        'actions',
        'events'
    ]

    """ List extensions """
    def admin_subscriptions(self, obj):
        return '<a href="../subscription/?newsletter__id__exact=%s">%s</a>' % (
                    obj.id, ugettext('Subscriptions'))
    admin_subscriptions.allow_tags = True
    admin_subscriptions.short_description = ''

    def admin_submissions(self, obj):
        return '<a href="../submission/?newsletter__id__exact=%s">%s</a>' % (
                    obj.id, ugettext('Submissions'))
    admin_submissions.allow_tags = True
    admin_submissions.short_description = ''

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(NewsletterAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        return field

class SubmissionAdmin(admin.ModelAdmin, ExtendibleModelAdminMixin):
    form = SubmissionAdminForm
    list_display = (
        'id',
        'admin_newsletter',
        'admin_publish_date',
        'publish',
        'admin_status_text',
        'admin_status',
        'admin_preview'
    )
    list_filter = (
        'newsletter',
        'publish',
        'sent'
    )
    filter_horizontal = (
        'subscriptions',
    )
    date_hierarchy = 'publish_date'
    save_as = True
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for sub in queryset:
            sub.submit()
    send_newsletter.short_description = _('Send test newsletter')

    """ List extensions """
    def admin_newsletter(self, obj):
        return '<a href="../newsletter/%s/">%s</a>' % (obj.newsletter.id, obj.newsletter)
    admin_newsletter.short_description = ugettext('newsletter')
    admin_newsletter.allow_tags = True

    def admin_publish_date(self, obj):
        if obj.publish_date:
            return date_format(obj.publish_date)
        else:
            return ''
    admin_publish_date.short_description = _("publish date")

    def admin_status(self, obj):
        if obj.prepared:
            if obj.sent:
                return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                        settings.ADMIN_MEDIA_PREFIX+'img/admin/icon-yes.gif', self.admin_status_text(obj))
            else:
                if obj.publish_date > datetime.now():
                    return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                        settings.STATIC_URL+'newsletter/admin/img/waiting.gif', self.admin_status_text(obj))
                else:
                    return u'<img src="%s" width="12" height="12" alt="%s"/>' % (
                        settings.STATIC_URL+'newsletter/admin/img/submitting.gif', self.admin_status_text(obj))
        else:
            return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                    settings.ADMIN_MEDIA_PREFIX+'img/admin/icon-no.gif', self.admin_status_text(obj))

    admin_status.short_description = _('admin status')
    admin_status.allow_tags = True

    def admin_status_text(self, obj):
        if obj.prepared:
            if obj.sent:
                return ugettext("Sent.")
            else:
                if obj.publish_date > datetime.now():
                    return ugettext("Delayed submission.")
                else:
                    return ugettext("Submitting.")
        else:
            return ugettext("Not sent.")
    admin_status_text.short_description = ugettext('Status')

    """ Views """
    def submit(self, request, object_id):
        submission = self._getobj(request, object_id)

        if submission.sent or submission.prepared:
            messages.add_message(request, messages.INFO, ugettext('Submission already sent.'))

            return HttpResponseRedirect('../../')

        submission.prepared=True
        submission.save()

        messages.add_message(request, messages.INFO, ugettext('Your submission is being sent.'))

        return HttpResponseRedirect('../../')

    def preview(self, request, object_id):
        return render_to_response(
            "newsletter/preview.html",
            { 'submission' : self._getobj(request, object_id) },
            RequestContext(request, {}),
        )

    def preview_html(self, request, object_id):
        submission = self._getobj(request, object_id)

        (subject_template, text_template, html_template) = \
            EmailTemplate.get_templates('message', submission.newsletter)

        if not html_template:
            raise Http404(_('No HTML template associated with the newsletter this message belongs to.'))

        c = Context({'site' : Site.objects.get_current(),
                     'newsletter' : submission.newsletter,
                     'date' : datetime.now(),
                     'STATIC_URL': settings.STATIC_URL,
                     'MEDIA_URL': settings.MEDIA_URL})

        return HttpResponse(html_template.render(c))

    def preview_text(self, request, object_id):
        submission = self._getobj(request, object_id)

        (subject_template, text_template, html_template) = \
            EmailTemplate.get_templates('message', submission.newsletter)

        c = Context({'site' : Site.objects.get_current(),
                     'newsletter' : submission.newsletter,
                     'date' : datetime.now(),
                     'STATIC_URL': settings.STATIC_URL,
                     'MEDIA_URL': settings.MEDIA_URL},
                     autoescape=False)

        return HttpResponse(text_template.render(c), mimetype='text/plain')

    def subscribers_json(self, request, object_id):
        submission = self._getobj(request, object_id)

        json = serializers.serialize("json", submission.newsletter.get_subscriptions(), fields=())
        return HttpResponse(json, mimetype='application/json')

    def admin_preview(self, obj):
        return '<a href="%d/preview/">%s</a>' % (obj.id, ugettext('Preview'))
    admin_preview.short_description = ''
    admin_preview.allow_tags = True

    """ URLs """
    def get_urls(self):
        urls = super(SubmissionAdmin, self).get_urls()

        my_urls = patterns('',
            url(r'^(.+)/preview/$',
                self._wrap(self.preview),
                name=self._view_name('preview')),
            url(r'^(.+)/preview/html/$',
                self._wrap(self.preview_html),
                name=self._view_name('preview_html')),
            url(r'^(.+)/preview/text/$',
                self._wrap(self.preview_text),
                name=self._view_name('preview_text')),
            url(r'^(.+)/submit/$',
                self._wrap(self.submit),
                name=self._view_name('submit')),
            url(r'^(.+)/subscribers/json/$',
                self._wrap(self.subscribers_json),
                name=self._view_name('subscribers_json')),
            )

        return my_urls + urls


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('title','action')
    list_display_links = ('title',)
    list_filter = ('action',)
    save_as = True

    form = EmailTemplateAdminForm


class SubscriptionAdmin(admin.ModelAdmin, ExtendibleModelAdminMixin):
    form = SubscriptionAdminForm
    list_display = (
        'name',
        'email',
        'admin_subscribe_date',
        'admin_unsubscribe_date',
        'admin_status_text',
        'admin_status',
    )
    list_display_links = (
        'name',
        'email',
    )
    list_filter = (
        'subscribed',
        'unsubscribed',
        'subscribe_date',
    )
    search_fields = (
        'name_field',
        'email_field',
        'user__first_name',
        'user__last_name',
        'user__email',
    )
    date_hierarchy = 'subscribe_date'

    """ List extensions """
    def admin_status(self, obj):
        if obj.unsubscribed:
            return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                        settings.ADMIN_MEDIA_PREFIX+'img/admin/icon-no.gif', self.admin_status_text(obj))

        if obj.subscribed:
            return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                        settings.ADMIN_MEDIA_PREFIX+'img/admin/icon-yes.gif', self.admin_status_text(obj))
        return u'<img src="%s" width="10" height="10" alt="%s"/>' % (
                        settings.STATIC_URL+'newsletter/admin/img/waiting.gif', self.admin_status_text(obj))

    admin_status.short_description = ''
    admin_status.allow_tags = True

    def admin_status_text(self, obj):
        if obj.subscribed:
            return ugettext("Subscribed")
        elif obj.unsubscribed:
            return ugettext("Unsubscribed")
        return ugettext("Unactivated")
    admin_status_text.short_description = ugettext('Status')

    def admin_subscribe_date(self, obj):
        if obj.subscribe_date:
            return date_format(obj.subscribe_date)
        return ''
    admin_subscribe_date.short_description = _("subscribe date")

    def admin_unsubscribe_date(self, obj):
        if obj.unsubscribe_date:
            return date_format(obj.unsubscribe_date)
        return ''
    admin_unsubscribe_date.short_description = _("unsubscribe date")


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
