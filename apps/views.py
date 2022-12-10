from django.contrib import redirects
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, FormView, DetailView, UpdateView

from apps.forms import RegistrationForm, LoginForm, ProfileForm
from apps.models import Category, Post, About, User


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


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'apps/signup.html'
    success_url = reverse_lazy('index')

    # next_page = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginPageView(LoginView):
    form_class = LoginForm
    fields = '__all__'
    template_name = 'apps/login.html'
    next_page = reverse_lazy('index')


class ProfileView(UpdateView):
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
