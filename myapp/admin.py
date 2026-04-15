from django.contrib import admin
from .models import Booking
from .models import Contact

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'service', 'date')
    search_fields = ('user__username', 'service')


from django.contrib import admin
from .models import Contact

admin.site.register(Contact)


