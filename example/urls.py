from django.urls import path
from .views import ListCreateFooView
from .views import UploadImageView, RetrieveImageView

urlpatterns = [
    path('foo/', ListCreateFooView.as_view(), name="foo-list-create"),
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('image/<int:pk>/', RetrieveImageView.as_view(), name='retrieve-image'),
]
