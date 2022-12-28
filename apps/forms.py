from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, PasswordInput, DateField, ModelForm, Form

from apps.models import User, Post, Comment, Message


class RegistrationForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput(attrs={"autocomplete": "current-password"}), )

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password == confirm_password:
            return make_password(password)
        raise ValidationError('Parol mos kemadi')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')


class LoginForm(AuthenticationForm):
    def clean_password(self):
        password = self.data.get('password')
        username = self.data.get('username')
        user = User.objects.get(username=username)
        if user and user.check_password(password):
            return password

        raise ValidationError('Parol yoki username mos kemadi')

    class Meta:
        model = User


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'avatar')


class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'category')


class ChangePasswordForm(ModelForm):
    def clean_password(self):
        user = self.instance
        new_pas = self.data.get('new_password')
        if user.check_password(self.data.get('password')):
            if new_pas == self.data.get('confirm_password'):
                return make_password(new_pas)

        raise ValidationError("Old or New password didn't match")

    class Meta:
        model = User
        fields = ('password',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class MessageForm(ModelForm):
    name = CharField(max_length=255)
    message = CharField()

    class Meta:
        model = Message
        fields = ('name', 'message')


class ForgotPasswordForm(Form):
    email = EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('This profile is not exist!')
        return email

    class Meta:
        model = User
        fields = ('email',)


class ResetPasswordForm(Form):
    confirm_password = CharField(widget=PasswordInput(attrs={"autocomplete": "current-password"}))

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if confirm_password != password:
            raise ValidationError('Parolni tekshiring!')
        return make_password(password)

    class Meta:
        model = User
        fields = ('password',)
