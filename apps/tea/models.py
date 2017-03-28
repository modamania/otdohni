from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import WithPublished, WithSite
from tinymce import models as tinymce_models
from tea.managers import InterviewManager
from sorl.thumbnail.fields import ImageWithThumbnailsField
from place.utils import gen_file_name


class Interview(WithPublished, WithSite):
    """ Intreview class inherited from WithPusblished """
    
    title = models.CharField(_('title'), max_length=250)
    image = ImageWithThumbnailsField(upload_to=gen_file_name,
        thumbnail={'size': (272, 128), 'options': {'crop':',10'}, 'quality': (100), 'subdir': '_thumb'},
        verbose_name=_('image'),
        blank=True, null=True)
    full_text = tinymce_models.HTMLField(_('full text'))

    objects = InterviewManager()

    class Meta:
        verbose_name = _('Interview')
        verbose_name_plural = _('Interviews')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """Returns absolute url
        for interview by id
        """
        return 'interview_detail', {}, {"interview_id" : self.pk}
    
