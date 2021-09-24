from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm
from user.models import Usuario


class UsuarioChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name',]


class PasswordChangeForm(PasswordResetForm):

    class Meta(PasswordResetForm):
        model = Usuario
        fields = ['password']