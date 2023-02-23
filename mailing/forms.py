from django import forms

from mailing.models import Mailing, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('time_mailing_start', 'time_mailing_end', 'period_mailing', 'status')

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['id_message'].queryset = Message.objects.filter(user=3)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
