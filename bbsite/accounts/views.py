from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django_filters import FilterSet

from accounts.forms import LoginForm, RegisterForm, ProfileUserForm, UserPasswordChangeForm, CommentUserForm
from bbapp.forms import CommentForm
from bbapp.models import Comment
from bbapp.utils import DataMixin


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Авторизация'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/registration.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('accounts:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'accounts/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user


# class ShowUserComments(FilterSet):
#     model = Comment
#     template_name = 'accounts/list_comments.html'
#     form_class = CommentUserForm
#     context_object_name = 'comm'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}
