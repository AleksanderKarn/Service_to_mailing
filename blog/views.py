from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Post


class PostListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        '''Переопределение метода get для
         добавления счетчика просмотров статей'''

        self.object = self.get_object()
        self.object.count_views += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'body', 'image']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_id = self.request.user.id
        post.save()
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body', 'image', 'is_active']
    success_url = reverse_lazy('home:home')


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home:home')
