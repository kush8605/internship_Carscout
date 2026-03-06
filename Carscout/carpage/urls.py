from django.urls import path
from . import views

urlpatterns = [
    path('userhome/',views.userhome,name='userhome'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('adminnav/',views.adminnav,name='adminnav'),
    path('usernav/',views.usernav,name='usernav'),
    path('',views.homepage,name='homepage'),
    path('cars/',views.car_listing,name='car_listing'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('cars/post/', views.post_car, name='post_car'),
    path('mycars/', views.my_listings, name='my_listing'),
    path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('cars/image/<int:image_id>/delete/', views.delete_car_image, name='delete_car_image'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),


]
