from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from jrweb.board.forms import PostingForm
from jrweb.board.models.post_models import Post


class PostCreateView(generic.CreateView):
    template_name = '../templates/board/post_new.html'
    form_class = PostingForm
    success_url = '/board/'

    def post(self, request, *args, **kwargs):
        view_name = 'create'
        contents_list = [view_name, self.get_form_kwargs()['data']]
        Post.objects.create(contents_list)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('board:index')
