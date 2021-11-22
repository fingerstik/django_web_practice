from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from jrweb.board.models.post_models import Post


class PostDeleteView(generic.DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/board/'

    def delete(self, request, *args, **kwargs):
        view_name = 'delete'
        contents_list = [view_name, self.get_object().pk]
        Post.objects.obj_delete(contents_list)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('board:index')

    def get(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)
