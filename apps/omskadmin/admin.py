from django.contrib import admin
from django.contrib.sites.models import Site

from django.utils.translation import ugettext_lazy as _
from models import SitesAdmin


class SiteOnlyAdmin(admin.ModelAdmin):

    filter_horizontal = ('sites',)

    def queryset(self, request):
        admin = SitesAdmin.objects.get(id=request.user.id)
        queryset = super(SiteOnlyAdmin, self).queryset(request)
        if not admin.sites.exists():
            return queryset
        else:
            return queryset.filter(sites__in=admin.sites.all()).distinct()

    def get_sites(self, obj):
        """Return the sites linked in HTML"""
        return ', '.join(['<a href="http://%(domain)s" target="blank">%(name)s</a>' %
                    site.__dict__ for site in obj.sites.all()])

    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')


class SitesAdminAdmin(admin.ModelAdmin):
    list_display = ['username', 'get_sites',]
    list_filter = [ 'username', 'sites__name',]
    search_fields = ['username', 'description',]
    filter_horizontal = ('sites',)
    exclude = ('is_superuser', 'last_login', 'password',
                'date_joined', 'user_permissions', 'is_active')

    def get_sites(self, lunch):
        """Return the sites linked in HTML"""
        return ', '.join(['<a href="http://%(domain)s" target="blank">%(name)s</a>' %
                    site.__dict__ for site in lunch.sites.all()])

    get_sites.allow_tags = True
    get_sites.short_description = _('site(s)')


admin.site.register(SitesAdmin, SitesAdminAdmin)
