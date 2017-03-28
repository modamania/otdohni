import random, logging

logger = logging.getLogger(__name__)

from datetime import datetime, timedelta

from django.db import models
from django.db.models import permalink
from django.template import Template, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.hashcompat import sha_constructor
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings

from tinymce import models as tinymce_models

from photoreport.models import PhotoReport
from news.models import NewsItem
from action.models import Action
from event.models import Event
from core.utils import slugify_filename

DATE_DELTA = {
     'pub_date__lte': datetime.now,
     'pub_date__gte':datetime.now() - timedelta(7)
 }


def make_activation_code():
    sha = sha_constructor(str(random.random())).hexdigest()[:5]
    sec = str(datetime.now().microsecond)
    return sha_constructor(sha + sec).hexdigest()


class Subscriber(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()

    def __unicode__(self):
        return "User %s" % self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('subscriber', None, {'object_id' : self.id})

    class Meta:
        ordering = [ "id" ]


class Newsletter(models.Model):
    title = models.CharField(max_length=80)
    logo = models.ImageField(verbose_name=u'Logo', upload_to=slugify_filename(prefix='maillist'), blank=True, null=True)
    photoreports = models.ManyToManyField(PhotoReport,
                            related_name='newsletters', null=True, blank=True)
    newsitems = models.ManyToManyField(NewsItem,
                                    related_name='newsletters')
    actions = models.ManyToManyField(Action,
                                    related_name='newsletters')
    events = models.ManyToManyField(Event,
                                    related_name='newsletters')

    text = tinymce_models.HTMLField(_('text'))
    visible = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True, unique=True)

    subscribe_template = models.ForeignKey('EmailTemplate',
                default=lambda: EmailTemplate.get_default_id('subscribe'),
                related_name='subcribe_template',
                verbose_name=_('subscribe template'),
                limit_choices_to={'action':'subscribe'})
    unsubscribe_template = models.ForeignKey('EmailTemplate',
                default=lambda: EmailTemplate.get_default_id('unsubscribe'),
                related_name='unsubcribe_template',
                verbose_name=_('unsubscribe template'),
                limit_choices_to={'action':'unsubscribe'})
    message_template = models.ForeignKey('EmailTemplate',
                default=lambda: EmailTemplate.get_default_id('message'),
                related_name='message_template',
                verbose_name=_('message template'),
                limit_choices_to={'action':'message'})

    def __unicode__(self):
        return "Newsletter %s" % self.title

    class Meta:
        ordering = [ "id" ]
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')

    @permalink
    def get_absolute_url(self):
        return ('newsletter', None, {'object_id' : self.id})

    @permalink
    def subscribe_url(self):
        return ('newsletter_subscribe_request', (),{})

    @permalink
    def unsubscribe_url(self):
        return ('newsletter_unsubscribe_request', (),{})

    def get_sender(self):
        return u'%s <%s>' % settings.NEWSLETTER_SENDER

    def get_subscriptions(self):
        logger.debug(_(u'Looking up subscribers for %s'), self)

        return Subscription.objects.filter(subscribed=True)

    def get_events(self):
        return self.events.order_by('category')

    @classmethod
    def get_default_id(cls):
        try:
            objs = cls.objects.all()
            if objs.count() == 1:
                return objs[0].id
        except:
            pass
        return None


class EmailTemplate(models.Model):
    ACTION_CHOICES = (
        ('subscribe', _('Subscribe')),
        ('unsubscribe', _('Unsubscribe')),
        ('message', _('Message')),
    )

    title = models.CharField(max_length=200, verbose_name=_('name'),
                            default=_('Default'))
    action = models.CharField(max_length=16, choices=ACTION_CHOICES,
                            db_index=True,
                            verbose_name=_('action'))

    subject = models.CharField(max_length=255, verbose_name=_('subject'))

    text = models.TextField(verbose_name=_('Text'),
                            help_text=_('Plain text e-mail message.\
                                        Available objects: date,\
                                        subscription, site, submission,\
                                        newsletter, STATIC_URL,\
                                        MEDIA_URL and message.'))
    html = tinymce_models.HTMLField(verbose_name=_('HTML'),
                            help_text=_('HTML e-mail alternative.'),
                            null=True,
                            blank=True)

    def __unicode__(self):
        return u"%s '%s'" % (self.get_action_display(), self.title)

    @classmethod
    def get_templates(cls, action, newsletter=None):
        assert action in ['subscribe', 'unsubscribe', 'message'],\
                                        'Unknown action %s' % action

        if newsletter:
            myemail = eval('newsletter.%s_template' % action)
        else:
            myemail = cls.objects.filter(action=action)[0]

        if myemail.html:
            return (Template(myemail.subject),
                        Template(myemail.text), Template(myemail.html))
        else:
            return (Template(myemail.subject), Template(myemail.text), None)

    class Meta:
        verbose_name = _('e-mail template')
        verbose_name_plural = _('e-mail templates')

        unique_together = ("title", "action")
        ordering = ('title', )

    @classmethod
    def get_default_id(cls, action):
        try:
            ls = EmailTemplate.objects.filter(action__exact=action)
            if ls.count() == 1:
                return ls[0].id
            else:
                ls = ls.filter(title__exact=_('Default'))
                if ls.count():
                    #There can be only one of these
                    return ls[0].id
        except:
            pass

        return None


class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'),
                                blank=True, null=True)
    ip = models.IPAddressField(_("IP address"),
                                blank=True, null=True)
    create_date = models.DateTimeField(editable=False,
                                default=datetime.now)
    activation_code = models.CharField(verbose_name=_('activation code'),
                                max_length=40,
                                default=make_activation_code)
    subscribed = models.BooleanField(verbose_name=_('subscribed'),
                                db_index=True,
                                default=False)
    subscribe_date = models.DateTimeField(verbose_name=_("subscribe date"),
                                null=True, blank=True)
    # This should be a pseudo-field, I reckon.
    unsubscribed = models.BooleanField(verbose_name=_('unsubscribed'),
                                db_index=True,
                                default=False)
    unsubscribe_date = models.DateTimeField(verbose_name=_("unsubscribe date"),
                                null=True, blank=True)
    name_field = models.CharField(verbose_name=_('name'),
                                help_text=_('optional'),
                                db_column='name', max_length=30,
                                blank=True, null=True)
    email_field = models.EmailField(db_column='email', verbose_name=_('e-mail'),
                                db_index=True, blank=True, null=True)

    def get_name(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.name_field

    def set_name(self, name):
        if not self.user:
            self.name_field = name
    name = property(get_name, set_name)


    def get_email(self):
        if self.user:
            return self.user.email
        return self.email_field

    def set_email(self, email):
        if not self.user:
            self.email_field = email
    email = property(get_email, set_email)

    def subscribe(self):
        logger.debug(u'Subscribing subscription %s.', self)
        self.subscribe_date = datetime.now()
        self.subscribed = True
        self.unsubscribed = False

    def unsubscribe(self):
        logger.debug(u'Unsubscribing subscription %s.', self)

        self.subscribed = False
        self.unsubscribed = True
        self.unsubscribe_date = datetime.now()

    def save(self, *args, **kwargs):
        assert self.user or self.email_field, _('Neither an email nor a\
                                                username is set. This asks\
                                                for inconsistency!')
        assert (self.user and not self.email_field)\
                or (self.email_field and not self.user),\
                _('If user is set, email must be null and vice versa.')

        # This is a lame way to find out if we have
        # changed but using Django API internals is bad practice.
        # This is necessary to discriminate from a state where
        # we have never been subscribed but is mostly
        # for backward compatibility. It might be very useful to
        # make this just one attribute 'subscribe' later.
        # In this case unsubscribed can be replaced by a method property.

        if self.pk:
            assert(Subscription.objects.filter(pk=self.pk).count() == 1)
            old_subscribed = Subscription.objects.get(pk=self.pk).subscribed
            old_unsubscribed = Subscription.objects.get(pk=self.pk).unsubscribed

            # If we are subscribed now and we used not to be so, subscribe.
            # If we user to be unsubscribed but are not so anymore, subscribe.
            if (self.subscribed and not old_subscribed)\
                    or (old_unsubscribed and not self.unsubscribed):
                self.subscribe()

                assert not self.unsubscribed
                assert self.subscribed

            # If we are unsubcribed now and we used not to be so, unsubscribe.
            # If we used to be subscribed but are not subscribed
            # anymore, unsubscribe.

            elif (self.unsubscribed and not old_unsubscribed)\
                    or (old_subscribed and not self.subscribed):
               self.unsubscribe()

               assert not self.subscribed
               assert self.unsubscribed
        else:
            if self.subscribed:
                self.subscribe()
            elif self.unsubscribed:
                self.unsubscribe()

        super(Subscription, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return _(u"%(name)s <%(email)s>") % {
                    'name': self.name, 'email': self.email}
        return _(u"%(email)s") % {'email': self.email}

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        unique_together = ('user', 'email_field')

    def get_recipient(self):
        if self.name:
            return u'%s <%s>' % (self.name, self.email)
        return u'%s' % (self.email)

    def get_sender(self):
        return u'%s <%s>' % settings.NEWSLETTER_SENDER

    def send_activation_email(self, action):
        assert action in ['subscribe', 'unsubscribe'], 'Unknown action'

        subject_template, text_template, html_template = \
            EmailTemplate.get_templates(action)

        variable_dict = {
            'subscription' : self,
            'site' : Site.objects.get_current(),
            'date' : self.subscribe_date,
            'STATIC_URL': settings.STATIC_URL,
            'MEDIA_URL': settings.MEDIA_URL,
        }

        unescaped_context = Context(variable_dict, autoescape=False)

        message = EmailMultiAlternatives(
            subject_template.render(unescaped_context),
            text_template.render(unescaped_context),
            from_email=self.get_sender(),
            to=[self.email]
        )

        if html_template:
            escaped_context = Context(variable_dict)

            message.attach_alternative(html_template.render(escaped_context),
                                      "text/html")

        message.send()

        logger.debug(u'Activation email sent for action\
                        "%(action)s" to %(subscriber)s\
                        with activation code "%(action_code)s".', {
                    'action_code':self.activation_code,
                    'action':action,
                    'subscriber':self,
        })

    @permalink
    def subscribe_activate_url(self):
        return ('newsletter_update_activate', (), {
            'email': self.email,
             'action' : 'subscribe',
             'activation_code' : self.activation_code
        })

    @permalink
    def unsubscribe_activate_url(self):
        return ('newsletter_update_activate', (), {
            'email': self.email,
            'action' : 'unsubscribe',
            'activation_code' : self.activation_code,
        })


class Submission(models.Model):
    newsletter = models.ForeignKey('Newsletter',
                                    verbose_name=_('newsletter'))
    subscriptions = models.ManyToManyField('Subscription',
                                    verbose_name=_('recipients'),
                                    help_text=_('If you select none,\
                                                the system will automatically\
                                                find the subscribers for you.'),
                                    db_index=True,
                                    limit_choices_to={'subscribed': True},
                                    blank=True)
    publish_date = models.DateTimeField(verbose_name=_('publication date'),
                                    db_index=True,
                                    default=datetime.now(),
                                    blank=True, null=True)
    publish = models.BooleanField(verbose_name=_('publish'),
                                    help_text=_('Publish in archive.'),
                                    db_index=True,
                                    default=True)
    prepared = models.BooleanField(verbose_name=_('prepared'),
                                    db_index=True,
                                    editable=False,
                                    default=False)
    sent = models.BooleanField(verbose_name=_('sent'),
                                    db_index=True,
                                    editable=False,
                                    default=False)
    sending = models.BooleanField(verbose_name=_('sending'),
                                    db_index=True,
                                    editable=False,
                                    default=False)

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')

    def __unicode__(self):
        return _(u"%(newsletter)s on %(publish_date)s") % {
            'newsletter': self.newsletter,
            'publish_date':self.publish_date,
        }

    def submit(self):
        subscriptions = self.subscriptions.filter(subscribed=True)

        logger.info(
                ugettext(u"Submitting %(submission)s to %(count)d people"), {
                    'submission': self,
                    'count': subscriptions.count()
        })

        assert self.publish_date < datetime.now(),\
                'Something smells fishy; submission time in future.'

        self.sending = True
        self.save()

        try:
            subject_template, text_template, html_template = \
                EmailTemplate.get_templates('message', self.newsletter)

            for subscription in subscriptions:
                variable_dict = {
                    'subscription' : subscription,
                    'site' : Site.objects.get_current(),
                    'submission' : self,
                    'newsletter' : self.newsletter,
                    'date' : self.publish_date,
                    'STATIC_URL': settings.STATIC_URL,
                    'MEDIA_URL': settings.MEDIA_URL
                }

                unescaped_context = Context(variable_dict, autoescape=False)

                message = EmailMultiAlternatives(
                    subject_template.render(unescaped_context),
                    text_template.render(unescaped_context),
                    from_email=self.newsletter.get_sender(),
                    to=[subscription.get_recipient()]
                )

                if html_template:
                    escaped_context = Context(variable_dict)

                    message.attach_alternative(
                        html_template.render(escaped_context),
                        "text/html"
                    )

                try:
                    logger.debug(ugettext(u'Submitting message to: %s.'), subscription)
                    message.send()
                except Exception, e:
                    logger.error(ugettext(u'Message %(subscription)s failed with error: %(error)s'), {
                                    'subscription': subscription,
                                    'error': e})

            self.sent = True

        finally:
            self.sending = False
            self.save()

    @classmethod
    def submit_queue(cls):
        todo = cls.objects.filter(prepared=True, sent=False, sending=False,
                                    publish_date__lt=datetime.now())
        for submission in todo:
            submission.submit()

    @classmethod
    def from_message(cls, newsletter):
        logger.debug(ugettext('Submission of newsletter %s'), newsletter)
        submission = cls()
        submission.newsletter = newsletter
        submission.save()
        submission.subscriptions = newsletter.get_subscriptions()
        return submission

    @permalink
    def get_absolute_url(self):
        return ('newsletter_archive_detail', (), {
                    'newsletter_slug': self.newsletter.slug,
                    'year': self.publish_date.year,
                    'month':self.publish_date.month,
                    'day':self.publish_date.day,
                    'slug':self.message.slug,
        })
