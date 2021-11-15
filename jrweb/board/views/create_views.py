from django.views import generic

from jrweb.board.forms import PostingForm


class PostingCreateView(generic.CreateView):
    template_name = 'board/new_posting.html'
    success_url = '/board/'
    form_class = PostingForm

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)
