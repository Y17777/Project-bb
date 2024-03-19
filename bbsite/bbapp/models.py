from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Bullets.PublishedStatus.PUBLISHED)


class Bullets(models.Model):
    class PublishedStatus(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=128, verbose_name='Заголовок')
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',
                              verbose_name='Фото', default=None, blank=True, null=True)
    content = RichTextField(blank=True, verbose_name='Контент')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    dateUpdate = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), PublishedStatus.choices)),
                                       default=PublishedStatus.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               related_name='posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Доска объявлений'
        verbose_name_plural = 'Доска объявлений'
        ordering = ['-dateCreation']
        indexes = [
            models.Index(fields=['-dateCreation'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads')


class Comment(models.Model):
    commentPost = models.ForeignKey(Bullets, on_delete=models.CASCADE, verbose_name='Статья')
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    commentAuthor = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='Автор статьи',
                                      related_name='comments', null=True, default=None)

    # rating = models.SmallIntegerField(default=0)
    def __str__(self):
        return f'{self.commentUser} : {self.text}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.commentPost_id})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



    # @property
    # def number_of_comments(self):
    #     return Comment.objects.filter(commentPost=self).count()

    # def like(self):
    #     self.rating += 1
    #     self.save()
    #
    # def dislike(self):
    #     self.rating -= 1
    #     self.save()
