from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/register/", views.registerView, name="register"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("home/", views.home_view, name="home"),
     path("protected/", views.ProtectedView.as_view(), name="protected")
    
]