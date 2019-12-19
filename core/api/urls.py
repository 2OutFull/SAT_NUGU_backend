from django.urls import path

from core.api.views import PengsuTeacher, PengsuListening

urlpatterns = [
    path("ask-question", PengsuTeacher.as_view()),
    path("eng-listening", PengsuListening.as_view()),
]
