from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import PostCreateView, \
    PostUpdateView, PostDeleteView, PostDetailView, PostListView

app_name = BlogConfig.name

urlpatterns = [
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('post_list/<int:pk>', cache_page(20)(PostDetailView.as_view()), name='post_detail'),
    path('post_list/', PostListView.as_view(), name='post_list'),
]
