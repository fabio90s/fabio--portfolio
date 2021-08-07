from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, FormView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Skills, Articles, Comments
from portfolio.models import Items
from . import forms
from .forms import PostForm, ContactForm, AddArticleForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect


# Create your views here.

def blogList(request):
    posts = Post.objects.all()
    topSkills = Skills.objects.all().exclude(description="").order_by('-level')
    otherSkills = Skills.objects.all().filter(description="")
    articles = Articles.objects.all().filter(
        visible=True).order_by('created_date')
    project = Items.objects.all()
    form = forms.ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['text']
            send_mail(
                'Contact Form',
                name + "\n" + email + "\n" + message,
                'settings.EMAIL_HOST_USER',
                ['fabivs9@gmail.com'],
                fail_silently=False,
            )
            messages.success(
                request, f"Thank you for getting in touch, {name}.")
            return redirect('blog:bloglist')
    context = {'posts': posts, 'topSkills': topSkills, 'otherSkills': otherSkills,
               'articles': articles, 'form': form, 'project': project}
    return render(request, 'blog/post_list.html', context)


def articleView(request, pk):
    articles = Articles.objects.get(id=pk)
    article = get_object_or_404(Articles, id=pk)
    comment = Comments.objects.all()
    comment_count = Comments.objects.count()
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('blog:viewarticle', pk)

    context = {'articles': articles,
               'form': form, 'comment': comment, 'comment_count': comment_count}
    return render(request, 'blog/article.html', context)


def addArticle(request):
    if not request.user.is_authenticated:
        raise Http404
    form = AddArticleForm()

    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            if instance.body.startswith("<p>"):
                instance.description = instance.body[3:150]
            elif instance.body.startswith("<"):
                instance.description = instance.body[4:150]
            else:
                instance.description = instance.body[0:150]
            instance.save()
            return redirect('blog:bloglist')
    context = {'form': form}
    return render(request, 'blog/add-article.html', context)


def modifyArticle(request, pk):
    article = Articles.objects.get(id=pk)
    if request.user != article.author:
        raise Http404

    form = AddArticleForm(instance=article)
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.body.startswith("<p>"):
                instance.description = instance.body[3:150]
            elif instance.body.startswith("<"):
                instance.description = instance.body[4:150]
            else:
                instance.description = instance.body[0:150]
            instance.save()
        messages.success(request, 'Updated!')
    context = {'form': form}
    return render(request, 'blog/edit-article.html', context)


def deleteArticle(request, pk):
    article = Articles.objects.get(id=pk)
    if request.user != article.author:
        raise Http404

    if request.method == 'POST':
        article.delete()
        return redirect("blog:bloglist")
    context = {'article': article}
    return render(request, 'blog/delete-article.html', context)


class MustBeAuthorGetObjectMixin:
    def get_object(self):
        obj = super().get_object()
        if obj.name != self.request.user:
            raise PermissionDenied("...")
        return obj


class CreateBlog(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:bloglist')


class UpdateBlog(LoginRequiredMixin, MustBeAuthorGetObjectMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:bloglist')


# class DeleteBlog(LoginRequiredMixin, MustBeAuthorGetObjectMixin, DeleteView):
#     model = Post
#     success_url = reverse_lazy('blog:bloglist')
#
#
# class BlogDetail(DetailView):
#     model = Post
