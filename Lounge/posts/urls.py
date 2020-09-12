from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('register', views.register, name='register'),
  path('login', views.login_view, name='login_view'),
  path('logout', views.logout_view, name='logout_view'),
  path('newpost', views.create_post, name='create_post'),
  path('newsub', views.create_sub, name='create_sub'),
  path('post-page<int:id>', views.post_page, name='post_page'),
  path('sub-<str:name>', views.sub_page, name='sub_page')
]