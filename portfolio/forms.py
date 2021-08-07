from .models import Items
from django.forms import ModelForm


class SiteCreateForm(ModelForm):

    class Meta:
        model = Items
        fields = '__all__'
        exclude = ['author']


class SiteUpdateForm(ModelForm):

    class Meta:
        model = Items
        fields = '__all__'
