from django.urls import path
from . import views 
from .views import AddPostView,PostUpdateView,AddCategoryView,DeletePostView,AddCommentView,DeleteCommentView

urlpatterns = [
    path('', views.home, name='home'),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('post/',AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('article/<int:pk>/delete',DeletePostView.as_view(), name='delete_post'),
    path('add_category/',AddCategoryView.as_view(), name='add_category'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='comments_post'),
    path('post/<int:post_id>/comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),
  
]
   



