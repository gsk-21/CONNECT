from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile
from django import forms


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address %s already exists, must be unique" % value)


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'id': "materialRegisterFormEmail"
                                               }, ),

            'email': forms.EmailInput(attrs={'class': 'form-control',
                                            'id': "materialRegisterFormEmail"
                                             }, ),

            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'id': 'materialRegisterFormFirstName'
                                                 }, ),

            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'id': "materialRegisterFormLastName"
                                                }, ),

            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'id': "materialRegisterFormPassword",
                                                   }, ),

        }

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if len(password) < 8:
            raise forms.ValidationError(
                "Your password must contain at least 8 characters"
            )
        elif password != confirm_password:
            raise forms.ValidationError(
                "Password mismatch"
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)
