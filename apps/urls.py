from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from apps import views
from apps.views import IndexView, BlogView, PostView, RegistrationView, LoginPageView, AboutView, ContactView, \
    ProfileView, AddPostView, MyPostsView, PdfView, ChangePasswordView, LeaveCommentView, ResetPasswordView, \
    ForgotPasswordPage, QrCodeView
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
      path('profile', ProfileView.as_view(), name='profile'),
      path('add-post', AddPostView.as_view(), name='add-post'),
      path('my-posts', MyPostsView.as_view(), name='my-posts'),
      path('pdf/<str:slug>', PdfView.as_view(), name='to_pdf'),
      path('change-password', ChangePasswordView.as_view(), name='change_password'),
      path('leave-comment', LeaveCommentView.as_view(), name='leave_comment'),

      path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
      path('forgot-password/', ForgotPasswordPage.as_view(), name='forgot'),
      path('reset/<str:uidb64>/<str:token>', ResetPasswordView.as_view(), name='reset'),
      path('qr_code/post/<str:slug>', PostView.as_view(), name='code')
  ] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
