from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('add-contact/<str:contact_username>/', views.add_contact, name='add_contact'),
    path('<str:contact_username>/', views.chat_view, name='chat'),  # For HTTP chat page
]
