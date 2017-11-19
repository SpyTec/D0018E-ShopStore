from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from profile.forms import ExtendedRegistrationForm


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
    form_class = ExtendedRegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()

        messages.add_message(self.request, messages.INFO, "Thanks for registering. You are now logged in.")
        new_user = authenticate(email=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'],
                                )
        login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)
