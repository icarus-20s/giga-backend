from django.contrib import admin
from django.utils.html import format_html
from myApp.models import Career, ContactMessage, CustomUser, EmailStorage, JobApplication,FAQ,GalleryImage

from django.contrib import admin
from .models import CustomUser, Notice, QuoteRequest

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'product_display')
    list_filter = ('role', 'product')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'product')

    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'product')
        }),
        ('Permissions', {
            'fields': ('role',)
        }),
    )
    def product_display(self, obj):
        return obj.get_product_display()
    product_display.short_description = "Product"

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employment_type', 'posted_on', 'deadline')
    list_filter = ('employment_type', 'posted_on', 'deadline')
    search_fields = ('title', 'location', 'description')
    date_hierarchy = 'posted_on'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'job', 'applied_date')
    list_filter = ('applied_date', 'job')
    search_fields = ('full_name', 'email')
    date_hierarchy = 'applied_date'

# Email Storage Admin
@admin.register(EmailStorage)
class EmailStorageAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'

# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    actions = ['mark_as_read', 'mark_as_unread']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    date_hierarchy = 'created_at'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'thumbnail', 'uploaded_at')
    search_fields = ('title',)
    readonly_fields = ('thumbnail', 'uploaded_at')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="object-fit: cover;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Preview"

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "service_name", "request_date")
    list_filter = ("request_date", "service_name")
    search_fields = ("full_name", "email", "service_name", "phone")
    ordering = ("-request_date",)
    readonly_fields = ("request_date",)

    # Optional: Customize the display in admin form
    fieldsets = (
        (None, {
            "fields": ("full_name", "email", "phone", "service_name", "message")
        }),
        ("Timestamps", {
            "fields": ("request_date",),
        }),
    )

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_at', 'has_pdf')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-date',)

    def has_pdf(self, obj):
        return bool(obj.pdf)
    has_pdf.boolean = True
    has_pdf.short_description = "PDF Uploaded"
