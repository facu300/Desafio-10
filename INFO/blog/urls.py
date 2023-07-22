from django.urls import path

from . import views



app_name = "blog"
urlpatterns = [
    path("", views.index_view, name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path("blog/", views.blog, name="blog"),
    path("blog/post", views.post, name="post"),
    # path("blog/register", views.register_view, name="register")
    path("blog/register", views.register_view, name="register")
]