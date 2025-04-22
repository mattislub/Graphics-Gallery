from datetime import (  # type: ignore
    datetime,
    timezone,
)

from django import forms  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from wagtail.users.forms import UserCreationForm, UserEditForm  # type: ignore

from core.models import User


class CustomUserEditForm(UserEditForm):

    is_active = forms.BooleanField(required=False, label=_('If user email is verified'), disabled=True)
    registration_date = forms.DateTimeField(required=False, label=_('Profile registration date'), disabled=True)
    verification_code = forms.CharField(required=False, label=_('Email verification code'), disabled=True)

    def __init__(self, *args, **kwargs) -> None:
        kwargs['editing_self'] = False
        super().__init__(*args, **kwargs)
        self.fields['balance'].disabled = True

        if self.instance and self.instance.pk:
            self.fields['registration_date'].initial = self.instance.registration_date

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'balance', 'is_active', 'verification_code', 'is_superuser', 'balance_replenishment_notification', 'purchase_notification', 'filled_cart_notification')


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['balance'].disabled = True

        self.fields['registration_date'].initial = datetime.now(tz=timezone.utc)

    is_active = forms.BooleanField(label=_('If user email is verified'), initial=True)
    registration_date = forms.DateTimeField(required=False, label=_('Profile registration date'), disabled=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'balance', 'is_active', 'is_superuser', 'balance_replenishment_notification', 'purchase_notification', 'filled_cart_notification')


class RegistrationUserForm(UserCreationForm):
    name = forms.CharField(required=True, label=_('First name and Last name'))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False

    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'email', 'password1', 'password2')
        exclude = ('first_name', 'last_name', 'is_superuser')

    def save(self, commit: bool = True) -> User:  # noqa FBT001, FBT002
        user = super(UserCreationForm, self).save(commit=False)
        name = self.cleaned_data['name']
        first_name, last_name = self.split_name(name)
        user.first_name = last_name
        user.last_name = first_name
        if commit:
            user.save()
        return user

    @staticmethod
    def split_name(name: str) -> tuple[str, str]:
        splited_name = name.split()
        last_name = splited_name[0]
        first_name = splited_name[1] if len(splited_name) > 1 else ''
        return first_name, last_name


class EditUserForm(UserEditForm):
    name = forms.CharField(required=True, label=_('First name and Last name'))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        del self.fields['first_name']
        del self.fields['last_name']
        del self.fields["is_superuser"]

    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'email', 'password1', 'password2', 'balance_replenishment_notification', 'purchase_notification', 'filled_cart_notification')

    def save(self, commit: bool = True) -> User:  # noqa FBT001, FBT002
        user = super().save(commit=False)
        name = self.cleaned_data['name']
        first_name, last_name = self.split_name(name)
        user.first_name = last_name
        user.last_name = first_name
        if commit:
            user.save()
        return user

    @staticmethod
    def split_name(name: str) -> tuple[str, str]:
        splited_name = name.split()
        last_name = splited_name[0]
        first_name = splited_name[1] if len(name) > 1 else ''
        return first_name, last_name
