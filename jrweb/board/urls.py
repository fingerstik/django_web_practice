from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.CallPostingView.as_view(), name="call_posting"),
    path('new_posting/', views.PostingCreateView.as_view(), name="new_posting"),
    path('<int:pk>/edit_posting/', views.PostingEditView.as_view(), name="edit_posting"),
    path('<int:pk>/delete_posting/', views.PostingDeleteView.as_view(), name="delete_posting"),
]
