from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from jrweb.board.forms import PostingForm
from jrweb.board.models import Posting


class PostingEditView(generic.UpdateView):
    model = Posting
    context_object_name = 'posting'
    template_name = 'board/edit_posting.html'
    success_url = reverse_lazy('board:call_posting')
    form_class = PostingForm

    def get_object(self):
        posting = get_object_or_404(Posting, pk=self.kwargs['pk'])

        return posting

    def get_success_url(self):
        return reverse('board:call_posting', kwargs={'pk': self.object.pk})
