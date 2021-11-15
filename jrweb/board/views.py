from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
# from django.utils.decorators import method_decorator
from django.views import generic
from jrweb.board.models import Posting
from jrweb.board.forms import PostingForm, LoginForm


# Create your views here.
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


class CallPostingView(generic.DetailView):
    model = Posting
    template_name = 'board/call_posting.html'

    def get_queryset(self):
        return Posting.objects.filter(posting_date__lte=timezone.now())


class PostingCreateView(generic.CreateView):
    template_name = 'board/new_posting.html'
    success_url = '/board/'
    form_class = PostingForm

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


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


class PostingDeleteView(generic.DeleteView):
    model = Posting
    context_object_name = 'posting'
    success_url = '/board/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# @method_decorator(logout_message_required, name='dispatch')
class LoginView(generic.FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    suceess_url = '/board/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)

        return super().form_valid(form)
