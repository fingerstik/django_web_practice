from django.utils import timezone
from django.views import generic

from jrweb.board.models.post_models import Post


class DetailView(generic.DetailView):
    model = Post
    template_name = 'board/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(date__lte=timezone.now())
