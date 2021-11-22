import logging
from datetime import timedelta

from django.contrib import messages
from django.db import models
from django.db.models import Q, F
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def get_searched_queryset(self, search_keyword, search_type):
        # print(self.model.title.field.get_prep_value)
        post_list = Post.objects.order_by('-pk')
        if search_keyword:
            if len(search_keyword) > 1:
                if search_type == 'all':
                    search_post_list = post_list.filter(Q(F(search_keyword in 'title')) |
                                                        Q(F(search_keyword in 'body')))
                elif search_type == 'title':
                    search_post_list = post_list.filter(F(search_keyword in 'title'))
                elif search_type == 'body':
                    search_post_list = post_list.filter(F(search_keyword in 'body'))
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
        my_title = contents_list[1]['title']
        my_body = contents_list[1]['body']
        # logging
        logger = logging.getLogger()
        if len(logger.handlers) <= 1:
            logger.setLevel(logging.INFO)
            my_format = logging.Formatter('%(asctime)s %(message)s')
            file_handler = logging.FileHandler('/mnt/d/workplace/Jetserve/jrweb/logfile.log')
            file_handler.setFormatter(my_format)
            logger.addHandler(file_handler)
        logger.info("{} {} {}".format(view_name, my_title, my_body))

    def create(self, contents_list):
        model_data = contents_list[1]
        self.obj_save(Post(), model_data['title'], model_data['body'])
        self.write_log(contents_list)

    def update(self, contents_list):
        obj = Post.objects.get(pk=contents_list[2])
        model_data = contents_list[1]
        self.obj_save(obj, model_data['title'], model_data['body'])
        self.write_log(contents_list[:-1])

    def obj_delete(self, contents_list):
        obj = Post.objects.get(pk=contents_list[1])
        contents_list[1] = {'title': obj.title, 'body': obj.body}
        self.write_log(contents_list)
        obj.delete()

    def obj_save(self, obj, title, body):
        obj.title = title
        obj.body = body
        obj.save()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_searched_queryset(self, search_keyword, search_type):
        return self.get_queryset().get_searched_queryset(search_keyword, search_type)

    def get_context_data(self, contents_list):
        return self.get_queryset().get_context_data(contents_list)

    def create(self, contents_list):
        return self.get_queryset().create(contents_list)

    def update(self, contents_list):
        return self.get_queryset().update(contents_list)

    def obj_delete(self, contents_list):
        return self.get_queryset().obj_delete(contents_list)

    def write_log(self, contents_list):
        return self.get_queryset().write_log(contents_list)


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    objects = PostManager()
