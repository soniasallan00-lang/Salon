from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Booking, UserProfile
from .forms import ContactForm, RegisterForm, ProfileEditForm
from django.utils import timezone




def index(request):
    return render(request, 'myapp/index.html')

def about(request):
    return render(request, 'myapp/about.html')

def services(request):
    return render(request, 'myapp/services.html')

def gallery(request):
    return render(request, 'myapp/gallery.html')

def team(request):
    return render(request, 'myapp/team.html')

@login_required(login_url='login')
def booking(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('salon_admin')
    if request.method == 'POST':
        service = request.POST.get('service')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        if service and date and time:
            # Store in session and redirect to payment page
            request.session['booking_data'] = {
                'service': service,
                'date': date,
                'time': time,
                'notes': notes,
            }
            return redirect('booking_payment')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'myapp/booking.html')


# Price map matching booking form options
SERVICE_PRICES = {
    'Haircut & Style': 275, 'Balayage': 1100, 'Keratin Smoothing': 2100,
    'Deep conditioning': 500, 'Designer Haircut': 270,
    'Holistic Facial Glow': 550, 'Deep Tissue Ritual': 1500,
    'Signature Glow Facial': 600, 'Delox Body Scrub': 800,
    'Bridal Makeup': 5500, 'Party Makeup': 1500, 'Daily Makeup': 600,
    'Bridal & Party Makeup': 7000, 'Basic Nail Polish Art': 500,
    'French Manicure': 700, 'Gel Nail Art': 2000,
    'Acrylic Nails Extensions': 7000, 'Dip Powder Nails': 2500,
    '3D Bridal Nails': 3000, 'Hair Cut Basic': 300, 'Hair Cut Advance': 700,
    'Hair Wash + Styling': 400, 'Beard Trim': 100, 'Beard Styling/Design': 300,
    'Clean Shave': 150, 'Hair Color': 1500, 'Beard Color': 500,
    'Highlights/Streaks': 3000, 'Cleanup': 400, 'Facial': 1000,
    'De Tan Facial': 1400, 'Head Massage': 550, 'Hair Spa': 700,
    'Body Massage': 1000, 'Manicure': 550, 'Pedicure': 750, 'Waxing': 700,
}

TIME_DISPLAY = {
    '09:00': '09:00 AM', '10:30': '10:30 AM', '12:00': '12:00 PM',
    '14:00': '02:00 PM', '15:30': '03:30 PM', '17:00': '05:00 PM',
}


@login_required(login_url='login')
def booking_payment(request):
    booking_data = request.session.get('booking_data')
    if not booking_data:
        return redirect('booking')

    service = booking_data.get('service', '')
    booking_data['price'] = SERVICE_PRICES.get(service, 0)
    booking_data['time_display'] = TIME_DISPLAY.get(booking_data.get('time', ''), booking_data.get('time', ''))

    return render(request, 'myapp/booking_payment.html', {'booking_data': booking_data})


@login_required(login_url='login')
def booking_confirm(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        notes = request.POST.get('notes', '')
        payment_method = request.POST.get('payment_method')
        price = request.POST.get('price', '')

        if service and date_str and time_str and payment_method:
            import random, string
            from datetime import datetime

            # Parse date and time strings into proper objects
            try:
                parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                parsed_date = date_str

            try:
                parsed_time = datetime.strptime(time_str, '%H:%M').time()
            except ValueError:
                parsed_time = time_str

            # Generate unique IDs
            booking_id = 'BK' + ''.join(random.choices(string.digits, k=8))
            transaction_id = ('TXN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                              if payment_method != 'cash' else None)
            receipt_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

            new_booking = Booking.objects.create(
                user=request.user,
                service=service,
                date=parsed_date,
                time=parsed_time,
                notes=notes,
                payment_method=payment_method,
                price=price,
                booking_id=booking_id,
                transaction_id=transaction_id,
                status='Pending',
            )
            request.session.pop('booking_data', None)

            if payment_method == 'cash':
                messages.success(request, f"Booking confirmed! Your Booking ID is {booking_id}. Pay at the salon.")
                return redirect('profile')
            else:
                return render(request, 'myapp/payment_slip.html', {
                    'booking': new_booking,
                    'receipt_no': receipt_no,
                })
        else:
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('booking')

    return redirect('booking')

def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def salon_admin(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related('user').order_by('-date', '-time')
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    today = timezone.now().date()
    return render(request, 'myapp/salon_admin.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'total': Booking.objects.count(),
        'confirmed': Booking.objects.filter(status='Confirmed').count(),
        'pending': Booking.objects.filter(status='Pending').count(),
        'rejected': Booking.objects.filter(status='Rejected').count(),
        'today_count': Booking.objects.filter(date=today).count(),
    })


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def admin_booking_action(request, booking_id, action):
    if request.method == 'POST':
        b = get_object_or_404(Booking, id=booking_id)
        if action == 'confirm':
            b.status = 'Confirmed'
            b.save()
            messages.success(request, f"Booking {b.booking_id or b.id} accepted.")
        elif action == 'reject':
            b.status = 'Rejected'
            b.save()
            messages.success(request, f"Booking {b.booking_id or b.id} rejected.")
        elif action == 'delete':
            b.delete()
            messages.success(request, "Booking deleted.")
    return redirect('salon_admin')


def sentmessage(request):
    return render(request, 'myapp/sentmessage.html')

def request_view(request):
    return render(request, 'myapp/request.html')

@login_required(login_url='login')
def profile(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('salon_admin')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'myapp/profile.html', {'bookings': user_bookings, 'profile': profile})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('salon_admin')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type', 'user')  # 'user' or 'admin'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if login_type == 'admin':
                if user.is_staff or user.is_superuser:
                    auth_login(request, user)
                    return redirect('salon_admin')
                else:
                    messages.error(request, "You do not have admin access.")
            else:
                if user.is_staff or user.is_superuser:
                    messages.error(request, "Admin accounts must use the Admin login.")
                else:
                    auth_login(request, user)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'myapp/login.html')

@login_required(login_url='login')
def profile_edit(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('salon_admin')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'myapp/profile_edit.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Welcome to The Better Feel!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')




from django.shortcuts import render, redirect
from django.contrib import messages   # 👈 add this
from .forms import ContactForm

@login_required(login_url='/login/') 
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "✨ Your message has been submitted successfully!")  # ✅

            return redirect('contact')

        else:
            messages.error(request, "❌ Something went wrong. Please try again.")

    else:
        form = ContactForm()

    return render(request, 'myapp/contact.html', {'form': form})
