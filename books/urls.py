from django.urls import path
from .views import (
    RegisterView,
    ProfileUpdateView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    HomePageView,
    DashboardView,
    ReviewCreateView,
    CustomLoginView
)

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views  

urlpatterns = [
    # Authentication and User Management
    path('', HomePageView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    #path('login/', LoginView.as_view(template_name='books/registration/login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),  # Redirect to login after logout
    #path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Dashboard route

    # Book Management
    path('book-list/', BookListView.as_view(), name='book-list'),  # Home page lists books
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),

    #Reviews
    path('<int:pk>/review/', ReviewCreateView.as_view(), name='review-create'),


    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='category-create'),
    path('categories/<int:pk>/update/', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),


    path('users/', views.user_list, name='user-list'),
    path('users/create/', views.user_create, name='user-create'),
    path('users/<int:pk>/update/', views.user_update, name='user-update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user-delete'),

]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='books/registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='books/registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='books/registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='books/registration/password_reset_complete.html'), name='password_reset_complete'),
]