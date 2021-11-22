from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name="post_detail"),
    path('post_new/', views.PostCreateView.as_view(), name="post_new"),
    path('<int:pk>/post_edit/', views.PostEditView.as_view(), name="post_edit"),
    path('<int:pk>/post_delete/', views.PostDeleteView.as_view(), name="post_delete"),
]
