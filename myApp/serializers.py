
from rest_framework import serializers
from myApp.models import (GalleryImage,ContactMessage, Career, JobApplication, QuoteRequest, Notice, FAQ ,EmailStorage)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = "__all__"

class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class EmailStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailStorage
        fields = "__all__"


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ["id", "title", "image", "uploaded_at"]
