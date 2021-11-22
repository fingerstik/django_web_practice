from django.views import generic

from jrweb.board.models.post_models import Post


class IndexView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = '../templates/board/index.html'
    context_object_name = 'post_list'

    # 검색하여 일치된 post 찾기
    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        return Post.objects.get_searched_queryset(search_keyword, search_type)

    # paginator, search index 찾아서 context로 출력
    def get_context_data(self, **kwargs):
        # # pagination
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        page = self.request.GET.get('page')
        contents_list = [context, search_keyword, search_type, page]
        return Post.objects.get_context_data(contents_list)
