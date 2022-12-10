from apps.models import About, Post, Category


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
