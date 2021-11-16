from django.contrib import admin

from jrweb.board.models.post_models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('posting context',  {'fields': ['title']}),
        (None,               {'fields': ['body']}),
        ('Date information', {'fields': ['date'], 'classes': ['collapse']}),
    ]
    list_display = (
        'title',
        'date'
    )
    list_filter = ['date']
    search_fields = ['title', 'body']
    readonly_fields = ['date']


admin.site.register(Post, PostAdmin)
