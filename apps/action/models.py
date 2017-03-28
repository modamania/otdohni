import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from sorl.thumbnail.fields import ImageField
from tinymce import models as tinymce_models

from djangosphinx.models import SphinxSearch
from common.models import WithPublished, WithSite
from managers import ActionManager, PollManager

ACTIONS_DIR = getattr(settings, 'ACTIONS_DIR', 'action')
ACTIONS_WINNER_DIR = getattr(settings, 'ACTIONS_WINNER_DIR', 'action_winner')


def make_poll_upload_path(instance, filename):
    """Generates upload path for FileField"""
    return u'%s/%s/%s' % (ACTIONS_DIR,
                        instance.poll.action.slug, filename)


def make_winner_upload_path(instance, filename):
    """Generates upload path for FileField"""
    print 'Yo'
    return u'%s/%s/%s' % (ACTIONS_WINNER_DIR,
                        instance.action.slug, filename)


class Action(WithPublished, WithSite):
    STATUS_TYPE = (
            (True, _('completed')),
            (False, _('not completed')),
    )
    title = models.CharField(_('title'), max_length=80)
    slug = models.SlugField(_('title slug'), unique=True)
    image = models.ImageField(_('image'), upload_to="action/%Y/%m", null=True, blank=True)
    short_text = models.TextField(_('short text for description'))
    full_text = tinymce_models.HTMLField(_('full text'))
    is_completed = models.BooleanField(_('status'), max_length=13,
                        choices=STATUS_TYPE,
                        default=False)

    search = SphinxSearch(
        index='action_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    objects = ActionManager()

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name = _('action')
        verbose_name_plural = _('actions')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Action, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('action_detail', args=[self.slug])


class Poll(WithPublished):
    STATUS_TYPE = (
            ('SOON', _('Poll will begin soon')),
            ('ACTIVE', _('Poll is active')),
            ('SUSPEND', _('Poll suspended')),
            ('COMPLETED', _('Poll finished')),
            ('NONE', _('Without poll, only work bidder')),
    )
    FREQUENCY_TYPE = (
        ('DAY', _('Once a day')),
        ('WEEK', _('Once a week')),
        ('ONCE', _('Only once')),
    )
    CAN_VOTE = (
        ('OLD', _('Only old users')),
        ('ALL', _('All users')),
    )
    AS_TABLE = 'table'
    AS_LIST = 'list'
    TYPE_CHOICE = (
        (AS_TABLE, _('Table')),
        (AS_LIST, _('List')),
    )
    MANY_TO_CHOICE = (
        ('ONE', _('One')),
        ('ALL', _('All')),
    )

    action = models.ForeignKey(Action, related_name='polls',
                        verbose_name=_('action'),
                        blank=True,
                        null=True)
    title = models.CharField(_('title'), max_length=80)
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    status = models.CharField(_('status'), max_length=10,
                    choices=STATUS_TYPE,
                    default='NONE')
    vote_frequency = models.CharField(_('Frequency'), max_length=10,
                    choices=FREQUENCY_TYPE,
                    default='ONCE')
    can_vote = models.CharField(_('Can vote'), max_length=10,
        choices=CAN_VOTE,
        default='ALL')
    display_type = models.CharField(_('Type of display'), max_length=5, choices=TYPE_CHOICE)
    many_to_choose = models.CharField(_('Many to choice'), max_length=3, \
        choices=MANY_TO_CHOICE, default='ALL')

    search = SphinxSearch(
        index='poll_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    objects = PollManager()

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('poll')
        verbose_name_plural = _('polls')

    def __unicode__(self):
        if self.action:
            return u'%s: %s' % (self.action.title, self.title)
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('poll_detail', args=[self.id])

    @property
    def is_actual(self):
        now = datetime.date.today()
        return now >= self.start_date and now < self.end_date

    @property
    def status_title(self):
        if self.status == 'SOON':
            return _('Poll will begin')
        elif self.status == 'ACTIVE':
            return _('Poll will until')
        elif self.status == 'SUSPEND':
            return _('Poll suspended')
        elif self.status == 'COMPLETED':
            return _('Poll finished')
        else:
            return ''

    def can_add_like(self, user, work):
        if not self.status == 'ACTIVE':
            return False
        if self.can_vote == 'OLD' and user.date_joined.date() > self.start_date:
            return False

        if self.many_to_choose == 'ALL':
            votes = work.work_votes.filter(user=user)
        else:
            votes = WorkBidderVote.objects.filter(user=user, \
                workbidder__in=(self.workbidders.all()))
        if not votes:
            return True

        if self.vote_frequency == 'ONCE':
            return False
        today = datetime.date.today()
        if self.vote_frequency == 'DAY' and today == votes[0].vote_date:
            return False
        if self.vote_frequency == 'WEEK' and today >= votes[0].vote_date \
            and today <= votes[0].in_a_week:
            return False
        return True


class Winner(models.Model):
    fio = models.CharField(_('FIO'), max_length=255)
    photo = ImageField(upload_to=make_winner_upload_path, null=True, blank=True)
    big_photo = ImageField(upload_to=make_winner_upload_path, null=True, blank=True)
    dt = models.DateField(_('date'), null=True, blank=True)
    action = models.ForeignKey(Action, related_name='winners')
    description = models.TextField(_('short text for description'), null=True, blank=True)

    class Meta:
        ordering = ['-dt']

    def __unicode__(self):
        return self.fio


class WorkBidder(models.Model):
    title = models.CharField(_('title'), max_length=80, blank=True, null=True)
    poll = models.ForeignKey(Poll, related_name='workbidders')
    author_name = models.CharField(_('author name'), max_length=80, blank=True, null=True)
    photo = ImageField(upload_to=make_poll_upload_path)
    text = tinymce_models.HTMLField(_('text'), blank=True, null=True)
    #user_likes = models.ManyToManyField(User, verbose_name=_('number votes'),
    #                        blank=True, null=True)
    total_likes = models.PositiveIntegerField(_('number of votes'), default=0)


    search = SphinxSearch(
        index='workbidder_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    class Meta:
        ordering = ['-total_likes']
        verbose_name = _('work bidder')
        verbose_name_plural = _('work bidders')

    def __unicode__(self):
        return u'%s - %s' % (self.poll, self.title)

    #@property
    #def get_total_likes(self):
    #    return self.user_likes.all().count()

class WorkBidderVote(models.Model):
    user = models.ForeignKey(User)
    workbidder = models.ForeignKey(WorkBidder, related_name='work_votes')
    vote_date = models.DateField(_('vote date'), auto_now_add=True)

    class Meta:
        ordering = ['-vote_date']

    @property
    def in_a_week(self):
        return self.vote_date + datetime.timedelta(days=7)

    def __unicode__(self):
        return self.workbidder.title