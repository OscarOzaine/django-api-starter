from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data
from .models import Foo
from .serializers import FooSerializer

from .models import UploadedImage
from .serializers import UploadedImageSerializer

class ListCreateFooView(generics.ListCreateAPIView):
    """
    GET foo/
    POST foo/
    """
    queryset = Foo.objects.all()
    serializer_class = FooSerializer

    @validate_request_data
    def post(self, request, *args, **kwargs):
        foo = Foo.objects.create(
            title=request.data["title"],
            description=request.data["description"]
        )
        return Response(
            data=FooSerializer(foo).data,
            status=status.HTTP_201_CREATED
        )

class UploadImageView(generics.CreateAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

class RetrieveImageView(generics.RetrieveAPIView):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer