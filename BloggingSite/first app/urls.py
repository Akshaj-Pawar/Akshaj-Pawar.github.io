from django.urls import path #importing a fucntion from the main django library
from firstapp import views #importing the views module from this folder
from firstapp.models import Posts

urlpatterns = [
    path('', views.index, name='home'),
    path('posts/<int:pk>/', views.post_content, name='post_page'), #this associates each post with its own private key which is displayed in the object table. Just edit the link to fit this new model.
    path('wip/', views.wip),
    path('like/<int:pk>/', views.like, name='like_post'),
    path('posts/<int:pk>/comment/', views.AddComment.as_view(), name='add_comment'),
    path('search/', views.Search, name='search')
    #<int:pk>
]