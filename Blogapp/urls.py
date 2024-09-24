from django.urls import path
from .views import BlogsView, PublicBlogView


urlpatterns = [
    path('blogs/', BlogsView.as_view()),
    path('blogs/public/', PublicBlogView.as_view())
]