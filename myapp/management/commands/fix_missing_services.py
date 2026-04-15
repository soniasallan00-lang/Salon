from django.core.management.base import BaseCommand
from django.db.models import Q
from myapp.models import Booking

class Command(BaseCommand):
    help = 'Fix bookings with missing service field by setting a default value.'

    def handle(self, *args, **options):
        default_service = 'Facial'  # Change as needed
        # Find bookings with empty service or null service
        bookings = Booking.objects.filter(Q(service='') | Q(service__isnull=True))
        count = bookings.count()
        
        # Update all at once
        Booking.objects.filter(Q(service='') | Q(service__isnull=True)).update(service=default_service)
        
        self.stdout.write(self.style.SUCCESS(f'Updated {count} bookings with service set to "{default_service}".'))
