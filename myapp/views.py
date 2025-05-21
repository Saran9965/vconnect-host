from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import empdata
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .models import Service
from .forms import ServiceForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Service, Rating, Review,models
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import EmpDataForm

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip().lower()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        address = request.POST.get('address', '').strip()
        contactno = request.POST.get('contactno', '').strip()
        location = request.POST.get('location', '').strip()
        if not all([name, email, password, address, contactno, location]):
            messages.error(request, "All fields are required!")
            return redirect('signup')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return redirect('signup')
        if not contactno.isdigit() or len(contactno) != 10:
            messages.error(request, "Invalid phone number. It must be exactly 10 digits.")
            return redirect('signup')
        if User.objects.filter(username=name).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or Email already exists!")
            return redirect('signup')
        user = User.objects.create_user(username=name, email=email, password=password)
        empdata.objects.create(
            name=name,
            email=email,
            password=password,
            address=address,
            contact_no=contactno,
            location=location)
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')
    return render(request, 'signup.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('name').lower()
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both fields are required!")
            return redirect('signup')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'signup.html')
        
def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required
def update_profile(request):
    try:
        profile = empdata.objects.get(email=request.user.email)
    except empdata.DoesNotExist:
        messages.error(request, 'Profile data not found.')
        return redirect('profile')

    if request.method == 'POST':
        form = EmpDataForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = EmpDataForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

def profile_view(request):
    emp_profile = None
    if request.user.is_authenticated:
        try:
            emp_profile = empdata.objects.get(user=request.user)
        except empdata.DoesNotExist:
            emp_profile = None

    context = {
        'user': request.user,
        'emp_profile': emp_profile
    }
    return render(request, 'profile.html', context)


def frontpage(request):
    return render(request,'frontpage.html')

def header(request):
    return render(request,'header.html')

def content(request):
    return render(request,'content.html')

def homepage(request):
    return render(request,'homepage.html')

def profile(request):
    return render(request,'profile.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.user = request.user
            service.save()
            messages.success(request, 'Service added successfully.')
            return redirect('add_service')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm()
    services = Service.objects.filter(user=request.user)
    return render(request, 'add_service.html', {'form': form, 'services': services})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)
    service.delete()
    messages.success(request, 'Service deleted successfully.')
    return redirect('add_service')

@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('add_service')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'add_service.html', {'form': form})

def plumber(request):
    selected_location = request.GET.get('location', '')
    services = Service.objects.filter(service_type='PLUMBER')
    if selected_location:
        services = services.filter(address__icontains=selected_location)
    for service in services:
        service.review = Review.objects.filter(service=service)
        service.average_rating = service.review.aggregate(models.Avg('rating'))['rating__avg']
    locations = Service.objects.filter(service_type='PLUMBER') \
                               .values_list('address', flat=True).distinct()
    return render(request, 'plumber.html', {
        'services': services,
        'locations': locations,
    })

def carpenter(request):
    selected_location = request.GET.get('location', '')
    services = Service.objects.filter(service_type='CARPENTER')
    if selected_location:
        services = services.filter(address__icontains=selected_location)
    for service in services:
        service.review = Review.objects.filter(service=service)
        service.average_rating = service.review.aggregate(models.Avg('rating'))['rating__avg']
    locations = Service.objects.filter(service_type='CARPENTER') \
                               .values_list('address', flat=True).distinct()
    return render(request, 'carpenter.html', {
        'services': services,
        'locations': locations,
    })

@login_required
def submit_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        if not rating or not review_text:
            return JsonResponse({'error': 'Rating and review are required.'}, status=400)
        Review.objects.create(
            service=service,
            user=request.user,
            rating=rating,
            text=review_text
        )
        # Update average rating for the service
        average_rating = service.review.aggregate(models.Avg('rating'))['rating__avg']
        service.average_rating = average_rating
        service.save()
        return JsonResponse({'message': 'Review submitted successfully!'})
    return JsonResponse({'error': 'Failed to submit review'}, status=400)

def electrician(request):
    selected_location = request.GET.get('location', '')
    services = Service.objects.filter(service_type='ELECTRICIAN')
    if selected_location:
        services = services.filter(address__icontains=selected_location)
    for service in services:
        service.review = Review.objects.filter(service=service)
        service.average_rating = service.review.aggregate(models.Avg('rating'))['rating__avg']
    locations = Service.objects.filter(service_type='ELECTRICIAN') \
                               .values_list('address', flat=True).distinct()
    return render(request, 'electrician.html', {
        'services': services,
        'locations': locations,
    })

def tvtech(request):
    selected_location = request.GET.get('location', '')
    services = Service.objects.filter(service_type='TV TECH')
    if selected_location:
        services = services.filter(address__icontains=selected_location)
    for service in services:
        service.review = Review.objects.filter(service=service)
        service.average_rating = service.review.aggregate(models.Avg('rating'))['rating__avg']
    locations = Service.objects.filter(service_type='TV TECH') \
                               .values_list('address', flat=True).distinct()
    return render(request, 'tvtech.html', {
        'services': services,
        'locations': locations,
    })

def plum(request):
    return render(request,'plum.html')

def elect(request):
    return render(request,'elect.html')

def tvtec(request):
    return render(request,'tv.html')

def carp(request):
    return render(request, 'carp.html')

@login_required
@csrf_exempt
def submit_rating(request, service_id):
    if request.method == "POST":
        service = get_object_or_404(Service, id=service_id)
        stars = request.POST.get('stars')
        if not stars:
            return JsonResponse({'success': False, 'error': 'Star value is required'})
        try:
            stars = int(stars)
            if stars < 1 or stars > 5:
                raise ValueError
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid star value'})

        rating_obj, created = Rating.objects.get_or_create(
            user=request.user,
            service=service,
            defaults={'stars': stars}
        )
        if not created:
            rating_obj.stars = stars
            rating_obj.save()
        all_ratings = Rating.objects.filter(service=service)
        total = sum(r.stars for r in all_ratings)
        count = all_ratings.count()
        service.avg_rating = total / count
        service.num_ratings = count
        service.save()
        return JsonResponse({'success': True, 'new_avg': service.avg_rating})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@csrf_exempt
def submit_review(request, service_id):
    if request.method == "POST":
        service = get_object_or_404(Service, id=service_id)
        data = json.loads(request.body)
        review_text = data.get('review')
        rating_val = data.get('rating')
        if not review_text or not rating_val:
            return JsonResponse({'error': 'Missing review or rating'}, status=400)
        Review.objects.create(
            user=request.user,
            service=service,
            rating=rating_val,
            review=review_text
        )
        return JsonResponse({'message': 'Review submitted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_reviews(request, service_id):
    reviews = Review.objects.filter(service_id=service_id).values(
        'rating', 'review', 'user__username', 'created_at')
    return JsonResponse({'reviews': list(reviews)})
