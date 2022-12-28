from datetime import datetime
from pyexpat import model

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models import TextField, CharField, ForeignKey, CASCADE, ImageField, DateField, RESTRICT, IntegerField, \
    BooleanField, SlugField, ManyToManyField, DateTimeField, JSONField, EmailField, TextChoices, Manager, Model, PROTECT
from django.utils.html import format_html
from django.utils.text import slugify


class User(AbstractUser):
    avatar = ImageField(upload_to='user', default='default/avatar.jpg')
    bio = TextField()
    gender = CharField(max_length=255)
    birthday = DateField(null=True, blank=True)
    phone = CharField(max_length=255, null=True, blank=True)
    social = JSONField(null=True, blank=True)
    subscribe = BooleanField(default=False)
    is_active = BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Foydalanuvchilar'
        verbose_name = 'Foydalanuvchi'


class Category(models.Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='category', default='default/default_post.jpg')
    slug = SlugField(max_length=255)

    class Meta:
        verbose_name_plural = 'Kategoriyalar'
        verbose_name = 'Kategoriya'

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

    class Meta:
        verbose_name_plural = 'Teglar'
        verbose_name = 'Teg'


class ActiveBlogsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Post.StatusChoice.ACTIVE)


class CancelBlogsManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=Post.StatusChoice.CANCEL)


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

    objects = Manager()
    active = ActiveBlogsManager()
    cancel = CancelBlogsManager()

    class Meta:
        verbose_name_plural = 'Postlar'
        verbose_name = 'Post'

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

    def update_views(self):
        self.views += 1
        self.save()
        return self.views

    def status_button(self):
        if self.status == self.StatusChoice.PENDING:
            return format_html(
                f"""<a href="active/{self.id}"> 
                        <input type="button" style="background-color: #4DB621;" value="active" name="status">
                    </a>
                    <a href="cancel/{self.id}">
                        <input type="button" style="background-color: #FF545E;" value="cancel" name="status">
                    </a>""")
        elif self.status == self.StatusChoice.ACTIVE:
            return format_html(
                """<a style="color: green; font-size: 1.10em;margin-top: 8px; margin: auto;">Activated</a>"""
            )
        return format_html(
            """<a style="color: #FF545E; font-size: 1.10em;margin-top: 8px; margin: auto;">Canceled</a>"""
        )


class Comment(models.Model):
    user = ForeignKey(User, on_delete=RESTRICT)
    text = RichTextUploadingField()
    created_at = DateTimeField(auto_now=True)
    post = ForeignKey(Post, on_delete=RESTRICT)

    class Meta:
        verbose_name_plural = 'Izohlar'
        verbose_name = 'Izoh'




class About(models.Model):
    title = CharField(max_length=255)
    image = ImageField(upload_to='about/')
    description = TextField()
    social = JSONField()
    short_description = TextField()
    location = CharField(max_length=255)
    phone = CharField(max_length=255)
    email = EmailField(max_length=255)


    class Meta:
        verbose_name_plural = 'Malumotlar'
        verbose_name = 'Biz haqimizda'

    def save(self, *args, **kwargs):
        for i, v in self.social.items():
            if not v.startswith('http'):
                self.social[i] = f'https://{v}'
        super().save(*args, **kwargs)


class Message(Model):
    author = ForeignKey(User, PROTECT)
    name = CharField(max_length=255)
    message = TextField()
    status = BooleanField(default=False)

    def __str__(self):
        return self.name


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region_id = IntegerField()
