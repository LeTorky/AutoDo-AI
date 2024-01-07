from django.urls import path
from .views.process_image_view import GetListFromImageView

urlpatterns = [
    path('list/', GetListFromImageView.as_view(), name='process'),
    # Add more URL patterns as needed
]
