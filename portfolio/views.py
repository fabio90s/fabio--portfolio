from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView, DeleteView
from .forms import SiteUpdateForm, SiteCreateForm
from .models import Items
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import Http404


class MustBeAuthorGetObjectMixin:
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied("...")
        return obj


def siteCreate(request):

    # item = Items.objects.all()
    # print(Items.author)
    if not request.user.is_authenticated:
        raise Http404
    form = SiteCreateForm()
    if request.method == 'POST':
        form = SiteCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()

        return redirect('blog:bloglist')
    context = {'form': form}
    return render(request, 'portfolio/portfolio_new.html', context)


class SiteUpdate(LoginRequiredMixin, MustBeAuthorGetObjectMixin, UpdateView):
    model = Items
    form_class = SiteUpdateForm
    success_url = reverse_lazy('blog:bloglist')


class SiteDelete(MustBeAuthorGetObjectMixin, DeleteView):
    model = Items
    success_url = reverse_lazy('blog:bloglist')


# Create your views here.
