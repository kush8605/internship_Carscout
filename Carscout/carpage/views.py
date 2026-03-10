from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from carpage.models import Car, CarImage, Inquiry, Message as ChatMessage,  TestDrive, Review, CarCompare
from django.contrib import messages
from .forms import CarForm, CarImageForm , EditProfileForm




# Create your views here.

@role_required(allowed_roles=["Buyer"])
def buyerhome(request):
    featured_cars = Car.objects.filter(
        is_verified=True, status='available'
    ).order_by('-created_at')[:8]

    recent_inquiries = Inquiry.objects.filter(
        buyer=request.user
    ).order_by('-created_at')[:3]

    recent_reviews = Review.objects.order_by('-created_at')[:4]

    brands = ['Maruti', 'Hyundai', 'Honda', 'Tata', 'Mahindra', 
              'Toyota', 'Ford', 'Volkswagen', 'BMW', 'Audi']

    return render(request, 'carpage/user/buyer/buyerhome.html', {
        'featured_cars': featured_cars,
        'recent_inquiries': recent_inquiries,
        'recent_reviews': recent_reviews,
        'active_inquiries': recent_inquiries.count(),
        'active_test_drives': TestDrive.objects.filter(buyer=request.user).count(),
        'brands': brands,
    })

@role_required(allowed_roles=["Buyer"])
def buyernav(request):
    return render (request,'carpage/user/buyer/buyernav.html')

@role_required(allowed_roles=["Admin"])
def adminhome(request):
    return render(request,'carpage/user/admin/adminhome.html')

@role_required(allowed_roles=["Admin"])
def adminnav(request):
    return render(request,'carpage/user/admin/adminnav.html') 


@role_required(allowed_roles=["Seller"])
def sellerhome(request):
    return render(request, 'carpage/user/seller/sellerhome.html')

@role_required(allowed_roles=["Seller"])
def sellernav(request):
    return render(request,'carpage/user/seller/sellernav.html')

def homepage(request):
    featured_cars = Car.objects.filter(
        is_verified=True,
        status='available'
    ).order_by('-created_at')[:8]

    recent_reviews = Review.objects.order_by('-created_at')[:4]

    brands = ['Maruti', 'Hyundai', 'Honda', 'Tata', 'Mahindra', 'Toyota', 'Ford', 'Volkswagen', 'BMW', 'Audi']

    return render(request, 'carpage/user/homepage.html', {
        'featured_cars': featured_cars,
        'recent_reviews': recent_reviews,
        'brands': brands,
    })

def publicnav(request):
    return render(request,'carpage/user/publicnav.html')


def car_listing(request):
    cars = Car.objects.filter(is_verified=True, status='available')

    # Filters
    brand = request.GET.get('brand')
    fuel = request.GET.get('fuel')
    transmission = request.GET.get('transmission')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if brand:
        cars = cars.filter(brand__icontains=brand)
    if fuel:
        cars = cars.filter(fuel_type=fuel)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if city:
        cars = cars.filter(city__icontains=city)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    return render(request, 'carpage/models/car_listing.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'carpage/models/car_detail.html', {'car': car})                  


@role_required(allowed_roles=["Seller"])
def post_car(request):
    car_form = CarForm()
    image_form = CarImageForm()

    if request.method == 'POST':
        car_form = CarForm(request.POST)
        image_form = CarImageForm(request.POST)

        if car_form.is_valid():
            car = car_form.save(commit=False)
            car.seller = request.user
            car.is_verified = False  # Admin verifies later
            car.save()

            # Save multiple images
            image_urls = request.POST.getlist('image_url[]')
            captions = request.POST.getlist('caption[]')

            for url, caption in zip(image_urls, captions):
               if url:  # only save if URL is not empty
                    CarImage.objects.create(
                        car=car,
                        image_url=url,
                        caption=caption
                    )

            messages.success(request, 'Car posted successfully! Waiting for admin approval.')
            return redirect('my_listing')

    return render(request, 'carpage/models/post_car.html', {
        'car_form': car_form,
        'image_form': image_form,
    })

@role_required(allowed_roles=["Seller"])
def my_listings(request):
    cars = Car.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'carpage/models/my_listing.html', {'cars': cars})


@role_required(allowed_roles=["Seller"])
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    car_form = CarForm(instance=car)

    if request.method == 'POST':
        car_form = CarForm(request.POST, instance=car)
        if car_form.is_valid():
            car_form.save()
            messages.success(request, 'Car updated successfully!')
            return redirect('my_listing')

    return render(request, 'carpage/models/edit_car.html', {'car_form': car_form, 'car': car})


@role_required(allowed_roles=["Seller"])
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)
    car.delete()
    messages.success(request, 'Car deleted successfully!')
    return redirect('my_listing')

@role_required(allowed_roles=["Seller"])
def delete_car_image(request, image_id):
    image = get_object_or_404(CarImage, id=image_id, car__seller=request.user)
    image.delete()
    messages.success(request, 'Image deleted!')
    return redirect('my_listing')


def profile(request):
    sold_count = 0
    if request.user.role == 'Seller':
        sold_count = request.user.cars.filter(status='sold').count()
    return render(request, 'carpage/models/profile.html', {
        'user': request.user,
        'sold_count': sold_count
    })


def edit_profile(request):
    if request.method == 'POST':
        # request.FILES handles the image upload automatically
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'carpage/models/edit_profile.html', {'form': form})



# Buyer sends first inquiry
@login_required
def send_inquiry(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if inquiry already exists
    existing = Inquiry.objects.filter(buyer=request.user, car=car).first()
    if existing:
        return redirect('inquiry_detail', inquiry_id=existing.id)
    
    # Create new inquiry
    inquiry = Inquiry.objects.create(
        buyer=request.user,
        car=car,
        status='open'
    )
    return redirect('inquiry_detail', inquiry_id=inquiry.id)


# Chat page
@login_required
def inquiry_detail(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)

    if request.user != inquiry.buyer and request.user != inquiry.car.seller:
        return redirect('car_listing')

    chat_messages = inquiry.messages.all()

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            ChatMessage.objects.create(
                inquiry=inquiry,
                sender=request.user,
                text=text
            )
            inquiry.messages.exclude(sender=request.user).update(is_read=True)
            return redirect('inquiry_detail', inquiry_id=inquiry.id)

    return render(request, 'carpage/models/inquiry_detail.html', {
        'inquiry': inquiry,
        'messages_list': chat_messages,
        'car': inquiry.car
    })

# All inquiries for buyer
@role_required(allowed_roles=["Buyer"])
def my_inquiries(request):
    inquiries = Inquiry.objects.filter(buyer=request.user).order_by('-created_at')

    status = request.GET.get('status')
    search = request.GET.get('search')

    if status:
        inquiries = inquiries.filter(status=status)
    if search:
        inquiries = inquiries.filter(
            car__brand__icontains=search
        ) | Inquiry.objects.filter(
            buyer=request.user,
            car__model__icontains=search
        )

    return render(request, 'carpage/models/my_inquiries.html', {
        'inquiries': inquiries
    })

# All inquiries for seller
@role_required(allowed_roles=["Seller"])
def seller_inquiries(request):
    inquiries = Inquiry.objects.filter(car__seller=request.user).order_by('-created_at')

    # Filters
    status = request.GET.get('status')
    search = request.GET.get('search')

    if status:
        inquiries = inquiries.filter(status=status)
    if search:
        inquiries = inquiries.filter(
            buyer__first_name__icontains=search
        ) | inquiries.filter(
            buyer__last_name__icontains=search
        ) | inquiries.filter(
            car__brand__icontains=search
        ) | inquiries.filter(
            car__model__icontains=search
        )

    return render(request, 'carpage/models/seller_inquiries.html', {
        'inquiries': inquiries
    })

# Update inquiry status
def update_inquiry_status(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['open', 'negotiating', 'closed']:
            inquiry.status = new_status
            inquiry.save()
    return redirect('inquiry_detail', inquiry_id=inquiry.id)


# Buyer books test drive
@login_required
def book_test_drive(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        notes = request.POST.get('notes')

        TestDrive.objects.create(
            buyer=request.user,
            car=car,
            date=date,
            time=time,
            location=location,
            notes=notes,
            status='pending'
        )
        messages.success(request, 'Test drive booked! Waiting for seller approval.')
        return redirect('my_test_drives')

    return render(request, 'carpage/models/book_test_drive.html', {'car': car})




# Buyer sees all their test drives
@login_required
def my_test_drives(request):
    test_drives = TestDrive.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'carpage/models/my_test_drives.html', {'test_drives': test_drives})


# Seller sees all test drives on their cars
@role_required(allowed_roles=["Seller"])
def seller_test_drives(request):
    test_drives = TestDrive.objects.filter(car__seller=request.user).order_by('-created_at')
    return render(request, 'carpage/models/seller_test_drives.html', {'test_drives': test_drives})


# Seller updates test drive status
@login_required
def update_test_drive(request, td_id):
    test_drive = get_object_or_404(TestDrive, id=td_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'scheduled', 'completed', 'cancelled']:
            test_drive.status = new_status
            test_drive.save()
            messages.success(request, f'Test drive marked as {new_status}!')

    return redirect('seller_test_drives')


# Buyer adds review on a car
@login_required
def add_review(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Check if buyer already reviewed this car
    existing = Review.objects.filter(reviewer=request.user, car=car).first()
    if existing:
        messages.error(request, 'You already reviewed this car!')
        return redirect('car_detail', car_id=car.id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating:
            Review.objects.create(
                car=car,
                reviewer=request.user,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Review added successfully!')
            return redirect('car_detail', car_id=car.id)

    return render(request, 'carpage/models/add_review.html', {'car': car})


# Delete review
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    car_id = review.car.id
    review.delete()
    messages.success(request, 'Review deleted!')
    return redirect('car_detail', car_id=car_id)  



def car_compare(request):
    cars = Car.objects.filter(is_verified=True, status='available')
    compare_data = None

    if request.method == 'POST':
        car1_id = request.POST.get('car1')
        car2_id = request.POST.get('car2')
        car3_id = request.POST.get('car3')

        car1 = get_object_or_404(Car, id=car1_id) if car1_id else None
        car2 = get_object_or_404(Car, id=car2_id) if car2_id else None
        car3 = get_object_or_404(Car, id=car3_id) if car3_id else None

        # Save compare to database
        if request.user.is_authenticated and car1 and car2:
            CarCompare.objects.create(
                user=request.user,
                car1=car1,
                car2=car2,
                car3=car3
            )

        compare_data = {
            'car1': car1,
            'car2': car2,
            'car3': car3,
        }

    return render(request, 'carpage/models/car_compare.html', {
        'cars': cars,
        'compare_data': compare_data
    })
 


