import datetime

from django.contrib import redirects
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, DetailView, UpdateView
from reportlab.pdfgen import canvas

from apps.forms import RegistrationForm, LoginForm, ProfileForm, AddPostForm, ChangePasswordForm, CommentForm, \
    ResetPasswordForm
from apps.models import Category, Post, About, User
from apps.utils import render_to_pdf


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


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'apps/auth/signup.html'
    success_url = reverse_lazy('index')
    redirect_authenticated_user = True

    # next_page = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
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


class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    success_url = reverse_lazy('profile')
    template_name = 'apps/auth/reset_password.html'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if user:
            user.is_active = False
            user.save()
        return super().post(request, *args, **kwargs)

