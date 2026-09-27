from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("run/<slug:job_name>/", views.run_job, name="run_job"),
]
