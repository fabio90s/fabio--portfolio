from .models import Post, Skills, Articles, Comments
from django.forms import ModelForm
from django import forms
from django.core.mail import send_mail


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['propic', 'text', 'location']


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    text = forms.CharField(widget=forms.Textarea())


class SkillForm(ModelForm):

    class Meta:
        model = Skills
        fields = '__all__'


class AddArticleForm(ModelForm):

    class Meta:
        model = Articles
        fields = ['title', 'image', 'body', 'visible']


class CommentForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['name', 'comment']
