from django.contrib.auth.forms import UsernameField, AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import CharField, EmailField, PasswordInput, DateField, ModelForm

from apps.models import User


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