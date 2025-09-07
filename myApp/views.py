import os
from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import check_password
from myApp.models import Career, GalleryImage, JobApplication, Notice, FAQ, CustomUser
from myApp.serializers import GalleryImageSerializer, LoginSerializer, CareerSerializer, JobApplicationSerializer,EmailStorageSerializer,QuoteRequestSerializer,NoticeSerializer, FAQSerializer, ContactSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from myApp.utils import send_email
from rest_framework.permissions import IsAuthenticated



@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = CustomUser.objects.filter(email=email).first()

    if not user or not check_password(password, user.password):
        return Response(
            data={"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "user": user.username,
            "role": user.role,
            "product": user.product,
            "message": "Login successful",
            "token": str(refresh.access_token),
        },
        status=status.HTTP_200_OK,
    )

@api_view(['POST'])
def contact_view(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        contact = serializer.save()
        try:
            submission_context = {
                    'name': contact.name,
                    'subject': "Thank you for contacting GigaInfosoft",
                    'to_emails' : [settings.DEFAULT_TO_EMAIL],
                    'message': contact.message,
                    'created_at': contact.created_at.strftime('%Y-%m-%d at %H:%M'),
                    'now': datetime.now(),
                    'template_name': 'email/contact_submission.html',
            }
            confirmation_context = {
                'name': contact.name,
                'subject': "Thank you for contacting GigaInfosoft",
                'to_emails' : [contact.email],
                'created_at': contact.created_at.strftime('%Y-%m-%d at %H:%M'),
                'now': datetime.now(),
                'template_name': 'email/contact_confirmation.html',
            }
            send_email(submission_context)
            send_email(confirmation_context)
            return Response({"message": "Your message has been sent successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": "Your message was saved but there was an issue sending the email notification."}, 
                           status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def notice_list(request):
    notices = Notice.objects.all().order_by('-date')
    serializer = NoticeSerializer(notices, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def notice_create(request):
    try:
        serializer = NoticeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "There was an error creating the notice."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def notice_delete(request, id):
    try:
        notice = Notice.objects.get(id=id)
    except Notice.DoesNotExist:
        return Response(
            {"message": "Notice not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    notice.delete()
    return Response({"message": "Notice deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def faq(request):
    faqs = FAQ.objects.all()
    serializer = FAQSerializer(faqs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def email_storage(request):
    serializer = EmailStorageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Listing all careers
@api_view(['GET'])
def career_listing(request):
    try:
        careers = Career.objects.all()
        serializer = CareerSerializer(careers, many=True)
        return Response(serializer.data)
    except:
        return Response(
            {"message": "No careers found"},
            status=status.HTTP_404_NOT_FOUND
        )

# Listing a specific career by its ID
@api_view(['GET'])
def career_listing_by_id(request, id):
    try:
        career = Career.objects.get(id=id)
        serializer = CareerSerializer(career)
        return Response(serializer.data)
    except:
        return Response(
            {"message": "Career not found"},
            status=404
        )
# Listing all job applications, grouped by job title
@api_view(['GET'])
def jobApplicationList(request):
    if request.method == 'GET':
        applications = JobApplication.objects.all()
        grouped_applications = {}

        for application in applications:
            job_title = application.job.title
            if job_title not in grouped_applications:
                grouped_applications[job_title] = []
            grouped_applications[job_title].append(application)

        # Prepare the response format
        grouped_data = {}
        for job_title, applications in grouped_applications.items():
            serializer = JobApplicationSerializer(applications, many=True)
            grouped_data[job_title] = serializer.data
        print(grouped_data)
        return Response(grouped_data)
    
    
@api_view(['GET'])
def jobApplicationDetail(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk)
    except JobApplication.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobApplicationSerializer(application)
        return Response(serializer.data)
    

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def gallery_admin_view(request):
    if request.method == 'GET':
        images = GalleryImage.objects.all().order_by('-uploaded_at')
        serializer = GalleryImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)

@api_view(["POST"])
def quote_request(request):
    try:
        serializer = QuoteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        data = serializer.validated_data
        context = {
            'subject': f"New Quote Request from {data.get('full_name')}",
            'fullName': data.get('full_name'),
            'email': data.get('email'),
            'to_emails': [settings.DEFAULT_TO_EMAIL],
            'phone': data.get('phone', 'Not provided'),
            'serviceName': data.get('service_name', ''),
            'message': data.get('message', 'No message provided'),
            'now': datetime.now(),
            'template_name': 'email/quote_request.html',
            
        }
        send_email(context)
        return Response(
            {"message": "Your request has been sent successfully!"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        print("Error in quote_request view:", e)
        return Response(
            {"error": "There was an error sending your request."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )