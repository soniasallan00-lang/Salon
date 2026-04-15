from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.get_or_create(user=instance)

class Booking(models.Model):
    SERVICE_CHOICES = [
        # Hair Care
        ('Haircut & Style', 'Haircut & Style'),
        ('Balayage', 'Balayage'),
        ('Keratin Smoothing', 'Keratin Smoothing'),
        ('Deep conditioning', 'Deep conditioning'),
        ('Designer Haircut', 'Designer Haircut'),
        # Skin & Spa
        ('Holistic Facial Glow', 'Holistic Facial Glow'),
        ('Deep Tissue Ritual', 'Deep Tissue Ritual'),
        ('Signature Glow Facial', 'Signature Glow Facial'),
        ('Delox Body Scrub', 'Delox Body Scrub'),
        # Makeup
        ('Bridal Makeup', 'Bridal Makeup'),
        ('Party Makeup', 'Party Makeup'),
        ('Daily Makeup', 'Daily Makeup'),
        ('Bridal & Party Makeup', 'Bridal & Party Makeup'),
        # Nail Arts
        ('Basic Nail Polish Art', 'Basic Nail Polish Art'),
        ('French Manicure', 'French Manicure'),
        ('Gel Nail Art', 'Gel Nail Art'),
        ('Acrylic Nails Extensions', 'Acrylic Nails Extensions'),
        ('Dip Powder Nails', 'Dip Powder Nails'),
        ('3D Bridal Nails', '3D Bridal Nails'),
        # Hair Services
        ('Hair Cut Basic', 'Hair Cut Basic'),
        ('Hair Cut Advance', 'Hair Cut Advance'),
        ('Hair Wash + Styling', 'Hair Wash + Styling'),
        # Beard Services
        ('Beard Trim', 'Beard Trim'),
        ('Beard Styling/Design', 'Beard Styling/Design'),
        ('Clean Shave', 'Clean Shave'),
        # Hair Color & Highlights
        ('Hair Color', 'Hair Color'),
        ('Beard Color', 'Beard Color'),
        ('Highlights/Streaks', 'Highlights/Streaks'),
        # Facial & Skin
        ('Cleanup', 'Cleanup'),
        ('Facial', 'Facial'),
        ('De Tan Facial', 'De Tan Facial'),
        # Spa & Massage
        ('Head Massage', 'Head Massage'),
        ('Hair Spa', 'Hair Spa'),
        ('Body Massage', 'Body Massage'),
        # Grooming
        ('Manicure', 'Manicure'),
        ('Pedicure', 'Pedicure'),
        ('Waxing', 'Waxing'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, blank=False, null=False)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Confirmed')
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    booking_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    transaction_id = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.service} on {self.date}"

    class Meta:
        ordering = ['date', 'time']

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name








