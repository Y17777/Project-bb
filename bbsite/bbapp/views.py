from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .filters import CommentFilterSet
from .forms import AddPostForm, UploadFileForm, CommentForm
from .models import Bullets, UploadFiles, Comment
from bbapp.utils import DataMixin


class BulletsHome(DataMixin, ListView):
    # model = Bullets
    template_name = 'bbapp/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Bullets.published.all().select_related('cat')


@login_required
def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'bbapp/about.html',
                  {'title': 'О сайте', 'form': form})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'bbapp/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        bb = form.save(commit=False)
        bb.author = self.request.user
        return super().form_valid(form)


class EditPage(LoginRequiredMixin, DataMixin, UpdateView):
    model = Bullets
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'bbapp/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    # permission_required = 'bbapp.change_bbapp'


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    permission_required = ('bbapp.delete_post',)
    # form_class = PostForm
    model = Bullets
    template_name = 'bbapp/deletepage.html'
    success_url = reverse_lazy('home')


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'bbapp/post.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = get_object_or_404(Bullets, pk=self.kwargs['pk'])
        comment.commentUser = self.request.user
        # comment.commentAutor = self.request.user
        # comment.text = self.request.text
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        author = User.objects.get(pk=post.author_id)
        send_mail(
            "Новый отклик на публикацию",
            f"Пользователь {comment.commentUser.username} откликнулся на Вашу публикацию {post}.",
            None,
            [author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs['pk']
        return context


class ShowPosts(DataMixin, DetailView, CreateComment):
    template_name = 'bbapp/post.html'
    # slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Bullets.published, pk=self.kwargs[self.pk_url_kwarg])


class ShowUserComments(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'bbapp/list_comments.html'
    # form_class = CommentFilterSet
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #         return context
        # context['filterset'] = CommentFilterSet(self.request.GET, queryset, request=self.request.user.id)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class BulletsCategory(DataMixin, ListView):
    template_name = 'bbapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Bullets.published.filter(cat=self.kwargs['pk']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
