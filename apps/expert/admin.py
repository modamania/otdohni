from django.contrib import admin
from expert.models import ExpertComment

class ExpertCommentAdmin(admin.ModelAdmin):

    list_display = ('author', 'category', 'is_published',)

admin.site.register(ExpertComment, ExpertCommentAdmin)


