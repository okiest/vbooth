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
            ('vertical',  _('Vertical Orientation')),
            ('horizontal',  _('Horizontal Orientation')),
            ('whole_strip',  _('Has printable strip')),
            ('half_strip',  _('Has single strip')),
        )
   
    def queryset(self, request, queryset):
        p = Photo.objects.all()
        ps = PhotoStrip.objects.all()
        has_photo = PhotoStrip.objects.filter(pk__in=[q.photo_strip.pk for q in p])
        whole = ps.exclude(strip_whole__exact='')
        half = ps.exclude(strip_half='')
        vertical = has_photo.filter(orientation="V")
        horizontal = has_photo.filter(orientation="H")
        if self.value() == 'images':
            return has_photo
        if self.value() == 'vertical':
            return vertical 
        if self.value() == 'horizontal':
            return horizontal 
        if self.value() == 'whole_strip':
            return whole 
        if self.value() == 'half_strip':
            return half 

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

class PhotoStripAdmin(admin.ModelAdmin):
    search_fields = ('strip_code',)
    list_display = ('strip_code', 'strip_date', 'strip_half', 'strip_whole',)
    list_filter = (PhotoStripFilter,)
    inlines = [
        PhotoInline,
    ]

admin.site.register(PhotoStrip, PhotoStripAdmin)
admin.site.register(Photo)
