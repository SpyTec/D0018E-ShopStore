from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from profile.models import User


class ExtendedRegistrationForm(UserCreationForm):

    class Meta:
        fields = [
            User.USERNAME_FIELD,
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'personal_id',
            'phone_number',
            'address',
            'city',
            'zip_code',
        ]
        model = User

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):

    class Meta:
        fields = [
            User.USERNAME_FIELD,
            'email',
            'password',
            'phone_number',
            'address',
            'city',
            'zip_code',
        ]
        model = User

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
