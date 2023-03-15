from django.urls import path

from .views import ProductUploadView

urlpatterns = [
    path('upload/', ProductUploadView.as_view(), name='upload'),
]
