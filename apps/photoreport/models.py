#coding: utf-8
import os

from apps.sorl.thumbnail.fields import ImageWithThumbnailsField
from django.contrib.auth.models import User
import os
import zipfile
import random
import string


from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.fields import ImageField

from djangosphinx.models import SphinxSearch
from tagging.models import Tag
from place.models import Place
from common.models import WithPublished, WithSite
from event.models import Event

from managers import PhotoReportManager
from place.utils import gen_file_name

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError('Gallery was unable to import the Python\
                            Imaging Library. Please confirm it`s\
                            installed and available on your current\
                            Python path.')


PHOTOREPORTS_DIR = getattr(settings, 'PHOTOREPORTS_DIR', 'photoreports')


def make_upload_path(instance, filename):
    """Generates upload path for FileField"""
    return u'%s/%s/%s' % (PHOTOREPORTS_DIR,
                        instance.photoreport.slug, filename)

def gen_file_name(filename):
    filetype = filename.split('.')[-1].lower()
    filename = ''.join([random.choice(string.digits + string.letters) for i in range(0, 10)])
    filename = '%s.%s' % (filename, filetype)
    return filename


class PhotoReport(WithPublished, WithSite):
    ON_MAIN_PAGE_CHOICES = (
        (True, _('On main page')),
        (False, _('Not on main page')),
    )

    event = models.ForeignKey(Event, related_name='photoreports',
                                blank=True, null=True)
    place = models.ForeignKey(Place, related_name='photoreports',
                                blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='photoreports',
                                verbose_name=_('tagging'),
                                blank=True, null=True)
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('title slug'), unique=True,
                                help_text=_('A "slug" is a unique URL-\
                                    friendly title for an object.'))
    description = models.TextField(_('description'), blank=True)
    date_event = models.DateField(_('date event'))
    num_photos = models.PositiveIntegerField(_('number of photos'),
                                default=0)
    on_mainpage = models.BooleanField(_('On mainpage'),
                                choices=ON_MAIN_PAGE_CHOICES,
                                default=False)

    search = SphinxSearch(
        index='photoreport_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    objects = PhotoReportManager()
    default_manager = models.Manager()

    class Meta:
        ordering = ['-date_event']
        get_latest_by = 'date_added'
        verbose_name = _('Photo report')
        verbose_name_plural = _('Photo reports')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        self.num_photos = self.get_num_photos()
        super(PhotoReport, self).save(*args, **kwargs)

    @property
    def place_event(self):
        if self.event:
            places = self.event.place.all()
            if places:
                return places[0]
        return None

    def get_absolute_url(self):
        return reverse('photoreport_detail', args=[self.slug])

    def get_preview(self):
        if self.photos.exists():
            return self.photos.order_by('?')[0]
        return None

    def get_num_photos(self):
        return self.photos.all().count()


class Photo(models.Model):
    photoreport = models.ForeignKey(PhotoReport,
                                    related_name='photos',
                                    verbose_name=_('Photo report'),
                                    null=True,
                                    blank=True)
    title = models.CharField(_('title'),
                                    max_length=100)
    slug = models.SlugField(_('slug'),
                                    unique=True,
                                    help_text=('A "slug" is a unique URL-friendly title for an object.'))
    caption = models.TextField(_('caption'),
                                    blank=True)
    date_added = models.DateTimeField(_('date added'),
                                    auto_now_add=True,
                                    editable=False)
    image = ImageField(upload_to=make_upload_path)

    search = SphinxSearch(
        index='photo_index',
        weights={
            'title': 100,
        },
        mode='SPH_MATCH_ALL',
        rankmode='SPH_RANK_NONE',
    )

    class Meta:
        ordering = ['date_added', 'id']
        get_latest_by = 'date_added'
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')

    @property
    def prev_photo(self):
        """Return the previous photo"""
        prev_photo = self.get_previous_by_date_added()
        if prev_photo in self.photoreport.photos.all():
            return prev_photo

    @property
    def next_photo(self):
        """Return the next photo"""
        next_photo = self.get_next_by_date_added()
        if next_photo in self.photoreport.photos.all():
            return next_photo

    @property
    def get_image(self):
        """Returns no_image.gif if image is blank"""
        return self.image if self.image else 'i/no_image.gif'

    def __unicode__(self):
        if self.photoreport:
            return u'%s: %s' % (self.photoreport.title, self.title)
        else:
            return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super(Photo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('photo_detail', args=[self.photoreport.slug, self.id])

class PhotoSubscribe(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    photo = models.ForeignKey(Photo, verbose_name=_('Photo'))

class PhotoReportUpload(models.Model):
    zip_file = models.FileField(_('images file (.zip)'),
                            upload_to=PHOTOREPORTS_DIR,
                            help_text=_('Select a .zip file of images to upload into a new photo report.'))
    photoreport = models.ForeignKey(PhotoReport,
                            null=True,
                            blank=True,
                            verbose_name=_('Photo report'),
                            help_text=_('Select a photo report to add these images to. leave this empty to create a new photo report from the supplied title.'))
    title = models.CharField(_('title'),max_length=75,
                            help_text=_('All photos in the photo report will be given a title made up of the photo report title + a sequential number.'))
    caption = models.TextField(_('caption'), blank=True,
                            help_text=_('Caption will be added to all photos.'))
    description = models.TextField(_('description'), blank=True,
                            help_text=_('A description of this photo report.'))

    class Meta:
        verbose_name = _('photo report upload')
        verbose_name_plural = _('photo report uploads')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(PhotoReportUpload, self).save(*args, **kwargs)
        photo = self.process_zipfile()
        super(PhotoReportUpload, self).delete()
        return photo

    def process_zipfile(self):
        if os.path.isfile(self.zip_file.path):
            if self.photoreport:
                photoreport= self.photoreport
            else:
                photoreport = PhotoReport.objects.create(title=self.title,
                                                 slug=slugify(self.title),
                                                 description=self.description,
                                                )
            count = photoreport.photos.count()+1
            title = '_'.join([photoreport.slug, str(count)])
            slug = slugify(title)
            photo = Photo(title=title,
                          slug=slug,
                          caption=self.caption,
                          photoreport=photoreport,
                          )
            while True:
                filename = gen_file_name(self.zip_file.name)
                filepath = make_upload_path(photo, filename)
                if not os.path.isfile(filepath):
                    break

            photo.image.save(filename, self.zip_file)
            photoreport.photos.add(photo)
            return photo
        return None

def denormalize_photos(sender, instance, created=False, **kwargs):
    try:
        instance.photoreport.num_photos = instance.photoreport.get_num_photos()
        instance.photoreport.save()
    except PhotoReport.DoesNotExist:
        print instance.id

models.signals.post_save.connect(denormalize_photos, sender=Photo)
models.signals.post_delete.connect(denormalize_photos, sender=Photo)
