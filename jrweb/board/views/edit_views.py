from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from jrweb.board.forms import PostingForm
from jrweb.board.models.post_models import Post


class PostEditView(generic.UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = '../templates/board/post_edit.html'
    success_url = reverse_lazy('board:post_detail')
    form_class = PostingForm

    def post(self, request, *args, **kwargs):
        view_name = 'edit'
        contents_list = [view_name, self.get_form_kwargs()['data'], self.get_object().pk]
        Post.objects.update(contents_list)
        return redirect(self.get_success_url())

    def get_object(self):
        posting = get_object_or_404(Post, pk=self.kwargs['pk'])

        return posting

    def get_success_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.get_object().pk})
