from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Post(models.Model):

    name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    location = models.CharField(max_length=256, null=True, blank=True)
    propic = models.ImageField(null=True, blank=True)
    text = RichTextUploadingField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Skills(models.Model):

    skill = models.CharField(max_length=256)
    description = RichTextUploadingField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    level = models.IntegerField(validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.skill


class Articles(models.Model):

    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(null=True, blank=True,
                              default='default-placeholder.png')
    body = RichTextUploadingField(blank=True)
    visible = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comments(models.Model):
    article = models.ForeignKey(
        'blog.Articles', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.TextField()
    allowed = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
