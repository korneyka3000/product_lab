from django.core.files import File
from rest_framework import serializers


def number_validator(value: str):
    if value.isdigit():
        return value
    else:
        raise serializers.ValidationError('This string field must contain only digits.')


def file_validator(file: File):
    if file.name.endswith('xlsx'):
        return file
    else:
        raise serializers.ValidationError('Unsupported file extension.')


class ProductSerializer(serializers.Serializer):
    file = serializers.FileField(required=False, validators=[file_validator])
    sku = serializers.CharField(max_length=255, required=False, validators=[number_validator])
