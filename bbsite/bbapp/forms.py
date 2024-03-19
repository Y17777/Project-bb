from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Bullets, Comment


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label="Выберите категорию",
                                 label='Категория')

    class Meta:
        model = Bullets
        fields = ['title', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 5}),
        }
        labels = {'slug': 'URL'}


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Dfj Комментарий',
        }
        widgets = {
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 2}),
        }
