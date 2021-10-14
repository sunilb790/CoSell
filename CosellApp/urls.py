from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView

urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:username>/',UserPostListView.as_view() , name='user-college-products'),
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('home', PostListView.as_view(), name='home'),
    path('product/<int:pk>/', PostDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', PostUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', PostDeleteView.as_view(), name='product-delete'),
    path('product/new/', PostCreateView.as_view(), name='product-create'),
    path('error', views.error, name='error'),
]
