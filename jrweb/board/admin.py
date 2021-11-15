from django.contrib import admin

from .models import Posting


# Register your models here.
class PostingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('posting context',  {'fields': ['posting_title']}),
        (None,               {'fields': ['posting_body']}),
        ('Date information', {'fields': ['posting_date'], 'classes': ['collapse']}),
    ]
    list_display = (
        'posting_title',
        'posting_date'
    )
    list_filter = ['posting_date']
    search_fields = ['posting_title', 'posting_body']
    readonly_fields = ['posting_date']


admin.site.register(Posting, PostingAdmin)
