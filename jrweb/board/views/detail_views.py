from django.utils import timezone
from django.views import generic

from jrweb.board.models import Posting


class CallPostingView(generic.DetailView):
    model = Posting
    template_name = 'board/call_posting.html'

    def get_queryset(self):
        return Posting.objects.filter(posting_date__lte=timezone.now())
