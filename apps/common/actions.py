from django.utils.translation import ugettext_lazy as _

def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)

make_published.short_description = _("Mark as published")


def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)

make_unpublished.short_description = _("Mark as unpublished")
