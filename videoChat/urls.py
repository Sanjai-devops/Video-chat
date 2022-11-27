from django.urls import path
from . import views

urlpatterns=[
    path('',views.lobby,name='lobby'),
    path('register',views.register,name='register'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout_page,name="signout"),
    path('room',views.room,name='room'),
    path('get_token',views.getToken,name='get_token'),
]