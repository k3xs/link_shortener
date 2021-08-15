from django.contrib import admin

from .models import Links, Feedback, UserModel


class LinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_url', 'shorten_url', 'time_create')
    list_display_links = ('id', 'original_url')
    search_fields = ('original_url',)


admin.site.register(Links, LinksAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    ordering = ['time_create']
    list_display = ('id', 'sender', 'status')
    search_fields = ['sender']
    list_filter = [
        ('status', admin.BooleanFieldListFilter),
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).all()


admin.site.register(Feedback, FeedbackAdmin)
