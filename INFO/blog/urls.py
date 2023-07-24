from django.urls import path

from . import views



app_name = "blog"
urlpatterns = [
    path("", views.index_view, name="index"),
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
    path("blog/", views.blog, name="blog"),
    path("post/<int:post_id>/", views.post, name="post"),
    # path("blog/register", views.register_view, name="register")
    path("blog/register", views.register_view, name="register"),
    path("blog/login", views.login_view, name="login"),
    path("blog/logout", views.logout_view, name="logout"),
    path("blog/new_post", views.new_post_view, name="new_post"),
    path("delete_comment/<int:comentario_id>/", views.delete_comment, name="delete_comment"),
    path('edit_users/', views.edit_users_permissions, name='edit_users_permissions'),
    path("post/<int:post_id>/editar/", views.editar_post, name="editar_post"),
    path("post/<int:post_id>/eliminar/", views.eliminar_post, name="eliminar_post"),

]
