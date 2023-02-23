from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import verify_email
from users.views import SigninView, SignupView, SignupSuccessView, UserEditProfileView, CustomPasswordResetView, \
    CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, UserListView, \
    change_status_user

app_name = UsersConfig.name

urlpatterns = [

    path('', SigninView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('register/success/', SignupSuccessView.as_view(), name='register_success'),
    path('verify/<str:token>/', verify_email, name='verify_email'),

    path('update_profile/', UserEditProfileView.as_view(), name='update_profile'),

    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/confirm/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('user/list/', UserListView.as_view(), name='user_list'),
    path('change-status/<int:pk>/', change_status_user, name='change_status'),
]
