from django.conf import settings
from django.core.cache import cache
from django.views.generic import TemplateView

from blog.models import Post
from mailing.models import Mailing
from subscriber.models import Subscriber
from users.models import User


class HomePageView(TemplateView):
    template_name = 'home.html'

    def _cache_subjects(self):
        queryset = Post.objects.filter(is_active=True).order_by('count_views')[:3]

        list_id_for_post = [] # список айдишников трех записей блога с наименьшим числом просмотров для унификации ключа для кеша
        for query in queryset:
            list_id_for_post.append(query.id)

        if settings.CACHE_ENABLED:
            key = f'fri_random_post_for_subject_{list_id_for_post[0]}_{list_id_for_post[1]}_{list_id_for_post[2]}'
            cache_data = cache.get(key)
            print("Данные из Кеша")
            if cache_data is None:
                cache_data = queryset
                cache.set(key, cache_data)
                print("Запись данных в Кеш")
            return cache_data
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list_all'] = Post.objects.all()
        context['mailing_list_runner'] = Mailing.objects.filter(status='runner')
        context['subscriber_list'] = Subscriber.objects.all()
        context['mailing_list'] = Mailing.objects.all()
        context['post_list'] = self._cache_subjects()
        return context
