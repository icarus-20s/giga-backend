from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from myApp.utils import upload_notice_pdf
class CustomUser(models.Model):
    ROLE_CHOICES=(
        ("admin","admin"),
    )
    PRODUCT_CHOICES=(
        ("gigaerp", "Giga ERP"),
        ("gigaaccounting", "Giga Accounting"),
        ("gigaims", "Giga IMS"),
        ("gigahrms", "Giga HRMS")
    )
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100,blank=True)
    last_name =models.CharField(max_length=100,blank=True)
    password =models.CharField(max_length=100)
    role = models.CharField(max_length=100,choices=ROLE_CHOICES)
    product = models.CharField(max_length=100,choices=PRODUCT_CHOICES)
    def save(self,*args,**kwargs):
        if self.password:
            self.password=make_password(self.password,hasher='bcrypt')
        super().save(*args,**kwargs)

    def __str__(self):
        return self.username
    

class EmailStorage(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Email Storage"
        verbose_name_plural = "Email Storage"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class Notice(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to=upload_notice_pdf, blank=True, null=True)

    def __str__(self):
        return self.title
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    


class QuoteRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service_name = models.CharField(max_length=150)  
    message = models.TextField(blank=True)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_name} ({self.request_date.strftime('%Y-%m-%d')})"



class Career(models.Model):
    JOB_TIME = [
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ]
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    employment_type = models.CharField(max_length=50, choices=JOB_TIME, default='Full-Time')
    posted_on = models.DateField(auto_now_add=True)
    deadline= models.DateField()
    
    def __str__(self):
        return f"{self.title} ({self.location})"
    
    class Meta:
        verbose_name = "Job Lisiting"
        verbose_name_plural = "job Listings"

    def clean(self):
        if self.deadline and self.deadline < now().date():
            raise ValidationError("The application deadline must be a future date.")
        
class JobApplication(models.Model):
    job = models.ForeignKey('Career', on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    resumes = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover-letters/', blank=True, null=True)
    applied_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Application for {self.job.title} by {self.full_name}"

    class Meta:
        verbose_name = "Applied Job Application"
        verbose_name_plural = "Applied Job Applications"




class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"
