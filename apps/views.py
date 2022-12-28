import datetime
import pyqrcode
import png
from pyqrcode import QRCode

from django.contrib import redirects
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse

from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView, UpdateView, CreateView
from reportlab.pdfgen import canvas
from django.contrib import messages
from apps.forms import RegistrationForm, LoginForm, ProfileForm, AddPostForm, ChangePasswordForm, CommentForm, \
    ForgotPasswordForm, ResetPasswordForm
from apps.models import Category, Post, About, User
from apps.utils import render_to_pdf
from apps.utils.tasks import send_to_gmail
from apps.utils.tokens import account_activation_token

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


class IndexView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories'] = Category.objects.all()
        context['last_post'] = Post.objects.order_by('-posted_at').first()
        context['last_posts'] = Post.objects.order_by('-posted_at').all()[1:5]
        context['url'] = reverse('blog')
        context['trending'] = enumerate(Post.objects.order_by('-views').all()[:5], 1)
        return context


class BlogView(ListView):
    queryset = Post.objects.all()
    template_name = 'apps/blog.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        slug = self.request.GET.get('category')
        context['categories'] = Category.objects.all()
        context['trending'] = enumerate(Post.objects.order_by('-views').all()[:5], 1)
        context['url'] = reverse('blog')
        context['category'] = Category.objects.filter(slug=slug).first()
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        if categ := self.request.GET.get('category'):
            return qs.filter(category__slug=categ)
        return qs


class AboutView(TemplateView):
    template_name = 'apps/about.html'


class ContactView(TemplateView):
    template_name = 'apps/contact.html'


class PostView(DetailView):
    queryset = Post.objects.all()
    template_name = 'apps/post.html'
    query_pk_and_slug = "slug"
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Post.objects.get(slug=slug)
        post.update_views()
        return super().get(request, *args, **kwargs)


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('apps/auth/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:

        uid = force_str(urlsafe_base64_decode(uidb64))  # uidb64='Tm9uZQ'
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login_page')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'apps/auth/signup.html'
    success_url = reverse_lazy('index')
    redirect_authenticated_user = True
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        obj = form.save(False)
        obj.is_active = False
        obj.save()
        activateEmail(self.request, obj, form.cleaned_data.get('email'))
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginPageView(LoginView):
    form_class = LoginForm
    fields = '__all__'
    template_name = 'apps/auth/login.html'
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'apps/profile.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return redirect('login_page')
        self.object = self.request.user
        context = self.get_context_data(object=self.object, form=self.form_class)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        return self.request.user


class AddPostView(LoginRequiredMixin, FormView):
    form_class = AddPostForm
    template_name = 'apps/add_post.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        obj = form.save(False)
        obj.user = self.request.user
        form.save()
        return super().form_valid(form)


class MyPostsView(LoginRequiredMixin, ListView):
    queryset = Post.objects.all()
    template_name = 'apps/blog.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        slug = self.request.GET.get('category')
        context['url'] = reverse('blog')
        context['category'] = Category.objects.filter(slug=slug).first()
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        if categ := self.request.GET.get('category'):
            return qs.filter(category__slug=categ)
        return qs


class ActivateEmailView(TemplateView):
    template_name = 'apps/auth/confirm_mail.html'

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.add_message(
                request=request,
                level=messages.SUCCESS,
                message="Your account successfully activated!"
            )
            return redirect('index')
        else:
            return HttpResponse('Activation link is invalid!')


class PdfView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        post = Post.objects.get(slug=slug)


        data = {
            'post': post
        }

        # Download
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="file.pdf"'
        # p = canvas.Canvas(response)
        # p.drawString(100, 800, f"{post.title}")
        # p.drawString(100, 770, f"{post.body}")
        # p.showPage()
        # p.save()
        # return response

        # to_pdf
        pdf = render_to_pdf('post-pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class ChangePasswordView(UpdateView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = self.request.user
        valid_form = super().form_valid(form)
        password = form.data.get('new_password')
        if conf := authenticate(username=user.username, password=password):
            login(self.request, conf)
            return render(self.request, 'apps/profile.html', {'res': True})
        return valid_form

    def form_invalid(self, form):
        return render(self.request, 'apps/profile.html', {'res': False})

    def get_object(self, queryset=None):
        return self.request.user


class LeaveCommentView(FormView):
    form_class = CommentForm
    success_url = reverse_lazy('post')

    # def get_object(self, queryset):
    #     return self.request.user

    def form_valid(self, form):
        obj = form.save(False)
        obj.user = self.request.user
        obj.post_id = form.data.get('post')
        form.save()
        return redirect(reverse('post', kwargs={'slug': obj.post.slug}))

    def form_invalid(self, form):
        return super().form_invalid(form)


class ForgotPasswordPage(FormView):
    template_name = 'apps/auth/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        activateEmail(self.request, self.request.user, form.cleaned_data.get('email'))
        return super().form_valid(form)


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'apps/auth/reset_password.html'
    success_url = reverse_lazy('login_page')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user:
            user.password = request.password
            user.save()
        return super().post(request, *args, **kwargs)

    # def get_user(self, uid, token):
    #     try:
    #         uid = force_str(urlsafe_base64_decode(uid))
    #         user = User.objects.get(pk=uid)
    #     except Exception as e:
    #         user = None
    #     return user, user and account_activation_token.check_token(user, token)
    #
    # def get(self, request, *args, **kwargs):
    #     user, is_valid = self.get_user(uid=kwargs.get('uidb64'), token=kwargs.get('token'))
    #     if not is_valid:
    #         return HttpResponse('Link not found')
    #     return super().get(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     user, is_valid = self.get_user(**kwargs)
    #     if is_valid:
    #         form = SetPasswordForm(user, request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('login')
    #     return HttpResponse('Link not found')


class QrCodeView(TemplateView):
    template_name = 'apps/post.html'
