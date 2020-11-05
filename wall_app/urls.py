from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('post_message', views.message),
    path('add_comment/<int:message_id>', views.comment),
    path('delete_comm/<int:comment_id>', views.delete_comment),
    path('delete_mess/<int:message_id>', views.delete_message),
]