from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html

from apps.models import Category, User, Tag, Comment, Post, About


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'images')

    def images(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="150" height="100">')


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'first_name')
    exclude = ('last_login', 'is_superuser', 'groups', 'user_permissions', 'date_joined', 'bio')


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('user',)


@admin.register(Post)
class PostAdmin(ModelAdmin):
    search_fields = ('category__name',)
    change_form_template = 'admin/change_post_form.html'

    list_display = ('title', 'user', 'views', 'categories', 'images', 'status_icon', 'status_button')
    exclude = ('slug',)

    def images(self, obj: Post):
        return format_html(f'<img src="{obj.image.url}" width="60" height="30">')

    def categories(self, obj: Post):
        tags_lst = [tag.name for tag in obj.category.all()]
        return format_html("<br>".join(tags_lst))

    def status_icon(self, obj):
        icons = {
            'pending': '<i class="fas fa-spinner fa-pulse" style="color: orange; font-size: 1.5em;"></i>',
            'cancel': '<i class="fa-solid fa-circle-xmark" style="color: red; font-size: 1.5em"></i>',
            'active': '<i class="fa-sharp fa-solid fa-circle-check" style="color: green; font-size: 1.5em"></i>'
        }
        return format_html(icons[obj.status])

    def get_urls(self):
        url = super().get_urls()
        url += [
            path('active/<int:id>', self.active),
            path('cancel/<int:id>', self.cancel)
        ]
        return url

    def active(self, request, id):
        post = Post.objects.get(id=id)
        post.status = Post.StatusChoice.ACTIVE
        post.save()
        return HttpResponseRedirect('../')

    def cancel(self, request, id):
        post = Post.objects.get(id=id)
        post.status = Post.StatusChoice.CANCEL
        post.save()
        return HttpResponseRedirect('../')

    def response_change(self, request, obj: Post):
        if request.POST.get('view'):
            return redirect('post', obj.slug)
        elif request.POST.get('status') in (Post.StatusChoice.ACTIVE, Post.StatusChoice.CANCEL):
            obj.status = request.POST.get('status').lower()
            obj.save()


        return super().response_change(request, obj)


@admin.register(About)
class AboutAdmin(ModelAdmin):
    list_display = ('title', 'image', 'phone', 'email')

