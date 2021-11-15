from django.contrib import messages
from django.views import generic

from jrweb.board.models import Posting


class IndexView(generic.ListView):
    model = Posting
    paginate_by = 5
    template_name = 'board/index.html'
    context_object_name = 'posting_list'

    def get_queryset(self):
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')
        posting_list = Posting.objects.order_by('-posting_date')

        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_posting_list = posting_list.filter(Q(posting_title__icontains=search_keyword) |
                                                              Q(posting_body__icontains=search_keyword))
                elif search_type == 'title':
                    search_posting_list = posting_list.filter(posting_title__icontains=search_keyword)
                elif search_type == 'body':
                    search_posting_list = posting_list.filter(posting_body__icontains=search_keyword)

                return search_posting_list
            else:
                messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
        return posting_list

    def get_context_data(self, **kwargs):
        # # pagination
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        # # search
        search_keyword = self.request.GET.get('q', '')
        search_type = self.request.GET.get('type', '')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type

        return context
