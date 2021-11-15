from django.views import generic

from jrweb.board.models import Posting


class PostingDeleteView(generic.DeleteView):
    model = Posting
    context_object_name = 'posting'
    success_url = '/board/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
