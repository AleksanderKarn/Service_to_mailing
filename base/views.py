from django.views.generic import TemplateView

from blog.models import Post
from mailing.models import Mailing
from subscriber.models import Subscriber


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list_all'] = Post.objects.all()
        context['mailing_list_runner'] = Mailing.objects.filter(status='runner')
        context['subscriber_list'] = Subscriber.objects.all()
        context['mailing_list'] = Mailing.objects.all()
        context['post_list'] = Post.objects.filter(is_active=True).order_by('-title')[:3]
        return context
