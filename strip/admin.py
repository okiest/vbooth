from django.contrib import admin
from django.db.models import F
from django.utils.translation import ugettext_lazy as _


from strip.models import *

class PhotoStripFilter(admin.SimpleListFilter):
    title = _('Filters')
    parameter_name = 'price type'

    def lookups(self, request, model_admin):
        return(
            ('images',  _('has photo')),
        )
   
    def queryset(self, request, queryset):
        p = Photo.objects.all()
        ps = PhotoStrip.objects.all()
        has_photo = PhotoStrip.objects.filter(pk__in=[q.photo_strip.pk for q in p])
        if self.value() == 'images':
            return has_photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

class PhotoStripAdmin(admin.ModelAdmin):
    search_fields = ('strip_code',)
    list_filter = (PhotoStripFilter,)
    inlines = [
        PhotoInline,
    ]

admin.site.register(PhotoStrip, PhotoStripAdmin)
admin.site.register(Photo)
