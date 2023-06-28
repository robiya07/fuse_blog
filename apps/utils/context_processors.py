from apps.models import About, Post, Category
from datetime import date


def custom_about(request):
    return {
        "custom_about": About.objects.first(),
    }


def custom_posts(request):
    return {
        "custom_posts": Post.objects.all()[:3],
    }


def custom_categories(request):
    return {
        "custom_categories": Category.objects.all()[:5],
    }


def custom_trending(request):
    return {"trending": enumerate(Post.objects.order_by('-views').all()[:5], 1)}


def this_year(request):
    return {'year': date.today().year}
