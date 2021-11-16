import logging
from datetime import timedelta

from django.contrib import messages
from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def get_searched_queryset(self, search_keyword, search_type):
        post_list = Post.objects.order_by('-pk')
        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_post_list = post_list.filter(Q(title__icontains=search_keyword) |
                                                        Q(body__icontains=search_keyword))
                elif search_type == 'title':
                    search_post_list = post_list.filter(title__icontains=search_keyword)
                elif search_type == 'body':
                    search_post_list = post_list.filter(body__icontains=search_keyword)
                return search_post_list
            else:
                messages.error(self, '검색어는 2글자 이상 입력해주세요.')
        return post_list

    def get_context_data(self, contents_list):
        context, search_keyword, search_type, page = contents_list
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        if start_index <= 1:
            context['index_before_page'] = 1
        else:
            context['index_before_page'] = start_index

        if end_index <= max_index - 1:
            context['index_next_page'] = end_index + 1
        else:
            context['index_next_page'] = max_index

        # # search
        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type

        return context

    def write_log(self, contents_list):
        view_name, form_string = contents_list
        # get_title_and_body
        form_string = list(map(str, str(form_string).replace("\n", "\"").replace("<", "\"").split("\"")))
        if len(form_string) >= 40:
            my_title, my_body = form_string[14], form_string[40]
        else:
            my_title, my_body = form_string[0], form_string[1]
        if len(my_title) == 0:
            my_title = '-'
        if len(my_body) == 0:
            my_body = '-'
        # logging
        logger = logging.getLogger()
        if len(logger.handlers) <= 1:
            logger.setLevel(logging.INFO)
            my_format = logging.Formatter('%(asctime)s %(message)s')
            file_handler = logging.FileHandler('/mnt/d/workplace/Jetserve/jrweb/logfile.log')
            file_handler.setFormatter(my_format)
            logger.addHandler(file_handler)
        logger.info("{} {} {}".format(view_name, my_title, my_body))


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_searched_queryset(self, search_keyword, search_type):
        return self.get_queryset().get_searched_queryset(search_keyword, search_type)

    def get_context_data(self, contents_list):
        return self.get_queryset().get_context_data(contents_list)

    def write_log(self, contents_list):
        return self.get_queryset().write_log(contents_list)


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def created_string(self):
        time = timezone.now() - self.date
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            return str(int(time.days)) + '일 전'
        else:
            return False

    objects = PostManager()
