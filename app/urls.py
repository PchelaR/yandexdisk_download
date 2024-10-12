from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import IndexView, LoginView, FileListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/<str:disk_id>/', FileListView.as_view(), name='file_list'),
]
