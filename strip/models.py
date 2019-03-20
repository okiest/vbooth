from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class PhotoStrip(models.Model):
    strip_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.strip_date)



class Photo(models.Model):
    photo_strip = models.ForeignKey('strip.PhotoStrip', on_delete=models.CASCADE)
    strip_image = models.ImageField(upload_to='media/', blank=True, null=True)

    def clean_content(self):
        content = self.cleaned_data['strip_image']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content._size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
        else:
            raise forms.ValidationError(_('File type is not supported'))
        return content
