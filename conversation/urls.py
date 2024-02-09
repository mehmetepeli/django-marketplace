from django.urls import path
from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:id>/', views.detail, name='detail'),
    path('new/<int:id>/', views.new_conversation, name='new'),
]