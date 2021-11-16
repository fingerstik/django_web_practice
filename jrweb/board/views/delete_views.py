from django.shortcuts import redirect
from django.views import generic

from jrweb.board.models.post_models import Post


class PostDeleteView(generic.DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/board/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk = self.object.pk
        view_name = 'delete'
        contents_list = [view_name, 'index<' + str(pk)]
        Post.objects.write_log(contents_list)
        self.object.delete()
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):

        return super().post(request, *args, **kwargs)
