from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy

from apps.views import IndexView, BlogView, PostView, RegistrationView, LoginPageView, AboutView, ContactView, ProfileView
from root.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('blog', BlogView.as_view(), name='blog'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('post/<str:slug>', PostView.as_view(), name='post'),
    path('register', RegistrationView.as_view(), name='register_page'),
    path('login', LoginPageView.as_view(), name='login_page'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout_page'),
    path('profile', ProfileView.as_view(), name='profile')
] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
