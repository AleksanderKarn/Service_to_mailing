from django.conf import settings
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

from users.forms import SigninForm, SignupForm, CustomEditUserForm, CustomPasswordResetForm
from users.models import User
from users.services import set_verify_token_and_send_mail


class SigninView(LoginView):
    template_name = 'users/login.html'
    form_class = SigninForm


class SignupView(CreateView):
    template_name = 'users/register.html'
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('users:register_success')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            set_verify_token_and_send_mail(self.object)
        return super().form_valid(form)


class SignupSuccessView(TemplateView):
    template_name = 'users/signup_success.html'


class UserEditProfileView(UpdateView):
    model = User
    template_name = 'users/update_users.html'
    form_class = CustomEditUserForm
    success_url = reverse_lazy('home:home')

    def get_object(self, queryset=None):
        """ при изменении профиля дает возможность
        не задавать ID пользователя и не светить его в URL """
        return self.request.user


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'password/email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/reset_complete.html'


class UserListView(ListView):
    model = User


def change_status_user(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active == True:
        user_item.is_active = False
    else:
        user_item.is_active = True
    user_item.save()

    return redirect(reverse('users:user_list'))
