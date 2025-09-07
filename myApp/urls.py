from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myApp.views import (
        contact_view, faq,login,
    career_listing, career_listing_by_id,jobApplicationList, jobApplicationDetail, email_storage,
    notice_list, quote_request,gallery_admin_view
)        

urlpatterns = [
    path("login/", login, name="login"),
    path('contact/', contact_view, name='contact'),
    path('gallery/', gallery_admin_view, name='gallery'),

      # Career (Job Listing) URLs
    path("career/", career_listing, name='career-list'),
    path("career/<int:id>/", career_listing_by_id, name='career-list-by-id'),

        # Job Application URLs
    path('jobapplications/', jobApplicationList, name='job-application-list'),
    path('jobapplication/<int:pk>/', jobApplicationDetail, name='job-application-detail'),
    path('quote/', quote_request, name='quote-request'),

        # Email storage URL
    path('emailstorage/', email_storage, name='email-storage'),
    path('notices/', notice_list, name='notice-list'),
    path('faqs/', faq, name='faqs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)