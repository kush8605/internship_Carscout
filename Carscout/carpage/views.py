from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from carpage.models import Car, CarImage
from django.contrib import messages
from .forms import CarForm, CarImageForm




# Create your views here.

@role_required(allowed_roles=["Buyer","Seller"])
def userhome(request):
    return render(request, 'carpage/user/userhome.html')

@role_required(allowed_roles=["Admin"])
def adminhome(request):
    return render(request,'carpage/admin/adminhome.html')

@role_required(allowed_roles=["Admin"])
def adminnav(request):
    return render(request,'carpage/admin/adminnav.html') 

@role_required(allowed_roles=["Buyer","Seller"])
def usernav(request):
    return render(request,'carpage/user/usernav.html')

def homepage(request):
    return render(request,'carpage/homepage.html')


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



