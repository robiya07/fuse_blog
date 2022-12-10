from datetime import datetime
from pyexpat import model

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import TextField, CharField, ForeignKey, CASCADE, ImageField, DateField, RESTRICT, IntegerField, \
    BooleanField, SlugField, ManyToManyField, DateTimeField, JSONField, EmailField, TextChoices
from django.utils.text import slugify


class User(AbstractUser):
    avatar = ImageField(upload_to='user', default='default/avatar.jpg')
    bio = TextField()
    gender = CharField(max_length=255)
    birthday = DateField(null=True, blank=True)
    phone = CharField(max_length=255, null=True, blank=True, unique=True)
    social = JSONField(null=True, blank=True)
    subscribe = BooleanField(default=False)


class Category(models.Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='category', default='default/default_post.jpg')
    slug = SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            while Post.objects.filter(slug=self.slug).exists():
                slug = Post.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self.name:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'

            super().save(*args, **kwargs)

    @property
    def post_count(self):
        return self.post_set.count()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    class StatusChoice(TextChoices):
        ACTIVE = 'active', 'Faol'
        CANCEL = 'cancel', 'Bekor qilindi'
        PENDING = 'pending', 'Kutilmoqda'

    title = CharField(max_length=255)
    body = RichTextUploadingField()
    posted_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    status = CharField(max_length=20, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    user = ForeignKey(User, on_delete=RESTRICT)
    category = ManyToManyField(Category)
    image = ImageField(upload_to='post/%m', default='default/default_post.jpg')
    views = IntegerField(default=0)
    slug = SlugField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

            while Post.objects.filter(slug=self.slug).exists():
                slug = Post.objects.filter(slug=self.slug).first().slug
                if '-' in slug:
                    try:
                        if slug.split('-')[-1] in self.title:
                            self.slug += '-1'
                        else:
                            self.slug = '-'.join(slug.split('-')[:-1]) + '-' + str(int(slug.split('-')[-1]) + 1)
                    except:
                        self.slug = slug + '-1'
                else:
                    self.slug += '-1'

            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    user = ForeignKey(User, on_delete=RESTRICT)
    text = RichTextUploadingField()
    created_at = DateTimeField(auto_now=True)
    post = ForeignKey(Post, on_delete=RESTRICT)


class About(models.Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='about/')
    description = TextField()
    social = JSONField()
    short_description = TextField()
    location = CharField(max_length=255)
    phone = CharField(max_length=255)
    email = EmailField(max_length=255)
