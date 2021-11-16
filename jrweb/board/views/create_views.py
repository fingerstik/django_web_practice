from django.shortcuts import redirect
from django.views import generic

from jrweb.board.forms import PostingForm
from jrweb.board.models.post_models import Post


class PostCreateView(generic.CreateView):
    template_name = 'board/post_new.html'
    form_class = PostingForm
    success_url = '/board/'

    def post(self, request, *args, **kwargs):
        view_name = 'create'
        contents_list = [view_name, self.get_form()]
        Post.objects.write_log(contents_list)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())
