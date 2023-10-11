from rest_framework import serializers

from .models import Foo
from .models import UploadedImage

class FooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foo
        fields = ("title", "description")

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'
