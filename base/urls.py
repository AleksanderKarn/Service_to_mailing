from django.urls import path

from base.apps import BaseConfig
from base.views import HomePageView

app_name = BaseConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
