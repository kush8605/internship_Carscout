from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import User


class Car(models.Model):
    FUEL_CHOICES = (
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('Electric', 'Electric'),
    )
    TRANSMISSION_CHOICES = (
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
    )
    CAR_STATUS = (
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    )
    OWNERSHIP_CHOICES = (
        (1, '1st Owner'),
        (2, '2nd Owner'),
        (3, '3rd Owner'),
        (4, '4th Owner or more'),
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    km_driven = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    color = models.CharField(max_length=30, blank=True)
    mileage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    engine_cc = models.PositiveIntegerField(blank=True, null=True)
    seating_capacity = models.PositiveIntegerField(default=5)
    ownership = models.PositiveIntegerField(choices=OWNERSHIP_CHOICES, default=1)
    city = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=CAR_STATUS, default='available')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'car_table'
        verbose_name_plural = 'Cars'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'car_image_table'
        verbose_name_plural = 'Car Images'

    def __str__(self):
        return f"Image for {self.car.brand} {self.car.model}"


class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('negotiating', 'Negotiating'),
        ('closed', 'Closed/Sold'),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_inquiries')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inquiries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inquiry_table'
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.buyer.email} → {self.car.brand} {self.car.model}"


class Message(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'message_table'
        ordering = ['sent_at']
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f"Message from {self.sender.email}"


class TestDrive(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_drives')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'test_drive_table'
        ordering = ['-date', '-time']
        verbose_name_plural = 'Test Drives'

    def __str__(self):
        return f"{self.buyer.email} → {self.car.brand} {self.car.model}"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_table'
        ordering = ['-created_at']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.reviewer.email} → {self.car.brand} ({self.rating}★)"


class CarCompare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car1 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='compare_car1')
    car2 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='compare_car2')
    car3 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='compare_car3', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'car_compare_table'
        verbose_name_plural = 'Car Comparisons'

    def __str__(self):
        return f"{self.user.email} comparing cars"


