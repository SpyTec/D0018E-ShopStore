from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from profile import forms


class Overview(LoginRequiredMixin, DetailView):
    template_name = 'profile/overview.html'

    def get_object(self, queryset=None):
        return self.request.user


class Orders(LoginRequiredMixin, DetailView):
    template_name = 'profile/orders.html'

    def get_object(self, queryset=None):
        return self.request.user


class RegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = forms.ExtendedRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()

        messages.info(self.request, "Thanks for registering. You are now logged in.")
        new_user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/edit.html'

    form_class = forms.EditProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()

        messages.info(self.request, "Profile has been saved.")
        return super(ProfileEditView, self).form_valid(form)


class PasswordChangeWithMessageView(PasswordChangeView):
    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed.")
        return super(PasswordChangeWithMessageView, self).form_valid(form)


class UserCart(LoginRequiredMixin, DetailView):
    template_name = 'profile/cart.html'

    def get_object(self, queryset=None):
        return self.request.user.cart
