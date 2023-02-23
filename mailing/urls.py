from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, MailingListView, \
    MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, MessageListView, change_status_mailing

app_name = MailingConfig.name

urlpatterns = [

    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_list/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),

    path('message_crate/', MessageCreateView.as_view(), name='message_create'),
    path('message_list/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),

    path('status/<int:pk>/', change_status_mailing, name='status'),

]
