from django.urls import path
from . import views
from subscriber.apps import ClientsConfig
from subscriber.views import SubscriberListView, SubscriberDetailView, SubscriberUpdateView, SubscriberCreateView, \
    SubscriberDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('subscriber_list/', SubscriberListView.as_view(), name='subscriber_list'),
    path('subscriber_list/<int:pk>/', SubscriberDetailView.as_view(), name='subscriber_detail'),
    path('subscriber_update/<int:pk>', SubscriberUpdateView.as_view(), name='subscriber_update'),
    path('subscriber_delete/<int:pk>', SubscriberDeleteView.as_view(), name='subscriber_delete'),
    path('subscriber_crate/', SubscriberCreateView.as_view(), name='subscriber_create'),

    path('mailings/add_subscriber/<int:pk>', views.add_subscribers_to_mailing, name='add_subscribers_to_mailing'),
    path('mailings/<int:pk>/add_subscriber/<int:subscriber_id>', views.mailing_add_subscriber,
         name='mailing_add_subscriber'),
    path('mailings/<int:pk>/del_subscriber/<int:subscriber_id>', views.mailing_del_subscriber,
         name='mailing_del_subscriber'),
]
