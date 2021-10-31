from django.utils import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from blog.models import Skills
# Create your models here.


class Items(models.Model):

    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256)
    description = RichTextUploadingField(blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True,
                              default='default-placeholder.png')
    tags = models.ManyToManyField(Skills, max_length=100, blank=True)
    created_date = models.DateTimeField(default=timezone.now)


    class Meta:

        ordering = ['-created_date']

    def __str__(self):
        return self.name
