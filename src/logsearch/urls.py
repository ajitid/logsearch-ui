from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("log_servers", views.log_servers),
    path("log_servers/count", views.log_servers_count),
    path("results/<uid>", views.results, name="results"),
    path("results/cached/<uid>", views.results_cached),
]
