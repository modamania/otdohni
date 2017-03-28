from rollyourown import seo
from django.utils.translation import ugettext_lazy as _

class Metadata(seo.Metadata):
    title       = seo.Tag(head=True)
    description = seo.MetaTag()
    keywords    = seo.KeywordTag()
    tooltip     = seo.MetaTag()
    heading     = seo.Tag(name="h1")
    paginator   = seo.Tag()

    class Meta:
        use_sites = True

    class HelpText:
        keywords = _('A comma separated list of words or phrases that describe the content')

