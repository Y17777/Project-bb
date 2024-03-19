from django import forms
from django.contrib import admin, messages

from django.utils.safestring import mark_safe

from .models import Bullets, Category, Comment

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BulletsAdminForm(forms.ModelForm):
    content = forms.CharField(label='Текст статьи', widget=CKEditorUploadingWidget())

    class Meta:
        model = Bullets
        fields = '__all__'


@admin.register(Bullets)
class BulletsAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'photo', 'post_photo', 'cat']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ["title"]}
    list_display = ('title', 'post_photo', 'cat', 'is_published')
    list_display_links = ('title',)
    ordering = ('-dateCreation', 'title')
    list_editable = ('is_published',)
    list_per_page = 15
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'content', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True
    form = BulletsAdminForm

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, bull: Bullets):
        if bull.photo:
            return mark_safe(f"<img src='{bull.photo.url}' width=50")
        return "Нет фото"

    @admin.action(description='Опубликовать выбранные')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Bullets.PublishedStatus.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description='Убрать из публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Bullets.PublishedStatus.DRAFT)
        self.message_user(request, f"{count} записей снято с публикации", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Comment)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    list_display_links = ('id', 'text')
