from django.contrib import admin
from .models import Car, CarImage, Inquiry, Message, TestDrive, Review, CarCompare


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3  # Shows 3 empty image slots when adding a car


class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price', 'city', 'status', 'is_verified', 'seller']
    list_filter = ['status', 'is_verified', 'fuel_type', 'transmission']
    search_fields = ['brand', 'model', 'city']
    inlines = [CarImageInline]  # Add images directly from car page


class InquiryAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'car', 'status', 'created_at']
    list_filter = ['status']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'inquiry', 'is_read', 'sent_at']


class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'car', 'date', 'time', 'status']
    list_filter = ['status']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'car', 'rating', 'created_at']


class CarCompareAdmin(admin.ModelAdmin):
    list_display = ['user', 'car1', 'car2', 'car3', 'created_at']


admin.site.register(Car, CarAdmin)
admin.site.register(CarImage)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(TestDrive, TestDriveAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CarCompare, CarCompareAdmin)

