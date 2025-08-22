from django.urls import path #importing a fucntion from the main django library
from UserAuth.views import RegisteringView

urlpatterns = [
    path('register/', RegisteringView.as_view(), name='register'),
]