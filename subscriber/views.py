from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.models import MailingToSubscriber, Mailing
from subscriber.models import Subscriber



### CRUD для сущности Subscriber


class SubscriberListView(ListView):
    model = Subscriber


class SubscriberDetailView(DetailView):
    model = Subscriber


class SubscriberCreateView(CreateView):
    model = Subscriber
    fields = ['email', 'full_name', 'comment']

    success_url = reverse_lazy('subscriber:subscriber_list')

    def form_valid(self, form):
        subscriber = form.save(commit=False)
        subscriber.user_id = self.request.user.id
        subscriber.save()
        return super(SubscriberCreateView, self).form_valid(form)


class SubscriberUpdateView(UpdateView):
    model = Subscriber
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('subscriber:subscriber_list')


class SubscriberDeleteView(DeleteView):
    model = Subscriber
    success_url = reverse_lazy('subscriber:subscriber_list')


def add_subscribers_to_mailing(request, pk):
    subscriber_to_mailing = {}
    for subscriber in MailingToSubscriber.objects.all().filter(mailing=pk):
        subscriber_to_mailing[subscriber.subscriber] = subscriber.mailing

    subscribers = []
    for subscriber in Subscriber.objects.all():
        if subscriber_to_mailing.get(subscriber.id):
            is_add = True
        else:
            is_add = False
        subscribers.append(
            {'id': subscriber.id, 'name': subscriber.full_name, 'email': subscriber.email, 'is_add': is_add,
             'user_id': subscriber.user_id})
    context = {
        'mailing': Mailing.objects.get(id=pk),
        'subscriber_list': subscribers,
    }
    return render(request, 'subscriber/mailing_add_subscriber_list.html', context)


def mailing_add_subscriber(request, pk, subscriber_id):
    if not MailingToSubscriber.objects.all().filter(mailing=pk, subscriber=subscriber_id).exists():
        new_record = MailingToSubscriber(mailing=pk, subscriber=subscriber_id)
        new_record.save()

    return redirect('subscriber:add_subscribers_to_mailing', pk)


def mailing_del_subscriber(request, pk, subscriber_id):
    MailingToSubscriber.objects.filter(mailing=pk, subscriber=subscriber_id).delete()
    return redirect('subscriber:add_subscribers_to_mailing', pk)
