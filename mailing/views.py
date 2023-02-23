from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.models import Mailing, Message, MailingToSubscriber, Attempt
from subscriber.models import Subscriber


def change_status():
    '''Функция для смены статуса
    рассылки с выполненной на запущенную при
    наступлении условия зависящего от периода каждой рассылки
    '''
    mail = Mailing.objects.all().filter(status='ended')
    for mailing in mail:

        if datetime.now().time() > mailing.time_mailing_start:
            continue
        if mailing.period_mailing == 'one_month' and datetime.now().day != 1:
            continue
        if mailing.period_mailing == 'one_month' and datetime.now().day != 1:
            continue

        mailing.status = Mailing.STATUS_RUN
        mailing.save()


def send_mailing(mailing):
    '''
    функция собирает айдишники подписчиков указанных в рассылке
    собирает в список их емайлы и производит рассылку на основании полученных данных
    :param mailing:
    :return:
    '''
    subscriber_id = MailingToSubscriber.objects.all().filter(mailing=mailing.id)
    _id = []
    for ids in subscriber_id:
        _id.append(ids.subscriber)

    subscribers = Subscriber.objects.all().filter(id__in=_id)
    subscriber_email = []
    for subscriber in subscribers:
        subscriber_email.append(subscriber.email)

    message = Message.objects.get(id=mailing.id_message_id)
    send_mail(
        subject=message.title,
        message=message.content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=subscriber_email
    )


def send_mails():
    '''
    функция берет все запущенные рассылки
    и проверяет время их завпуска и в случае если наступает период запуска рассылки
    она меняет статус рассылки на исполнена и формируект Attempt(попытку рассылки)
    :return:
    '''
    mailings = Mailing.objects.all().filter(status=Mailing.STATUS_RUN)
    for mailing in mailings:
        if datetime.now().time() > mailing.time_mailing_start:
            try:
                send_mailing(mailing)
                mailing.status = Mailing.STATUS_END
                mailing.save()
                answer = 200
                status_attempt = 'Успех'
            except:
                answer = 500
                status_attempt = 'Фейл'
            Attempt.objects.create(mailing_id=mailing.id, answer=answer, status_attempt=status_attempt)


# def castomer_cron_for_windows():
#    '''
#    функция таймер запускающая скрипты через
#     указанные промежутки времени
#    :return:
#    '''
#    change_status()
#    send_mails()
#    nt = Timer(60, castomer_cron_for_windows)
#    nt.start()
#
#
# castomer_cron_for_windows()

### CRUD для сущности Mailing

class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ['time_mailing_start', 'time_mailing_end', 'period_mailing', 'status', 'id_message']
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user_id = self.request.user.id
        mailing.save()
        return super(MailingCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['id_message'].queryset = Message.objects.filter(user=self.request.user)
        return context


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['time_mailing_start', 'time_mailing_end', 'period_mailing', 'status', 'id_message']
    success_url = reverse_lazy('mailing:mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return mailing.concreted_user == self.request.user or self.request.user.has_perms(perm_list=['off_mailing'])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    ### CRUD для сущности Message


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.user_id = self.request.user.id
        message.save()
        return super(MessageCreateView, self).form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


def change_status_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.status == 'create':
        mailing_item.status = 'runner'
    elif mailing_item.status == 'runner':
        mailing_item.status = 'ended'
    else:
        mailing_item.status = 'create'
    mailing_item.save()

    return redirect(reverse('mailing:mailing_list'))
