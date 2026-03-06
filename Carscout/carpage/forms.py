from django import forms
from carpage.models import Car, CarImage
from core.models import User


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'brand', 'model', 'year', 'price', 'km_driven',
            'fuel_type', 'transmission', 'color', 'mileage',
            'engine_cc', 'seating_capacity', 'ownership',
            'city', 'description'
        ]
        widgets = {
            'brand':            forms.TextInput(attrs={'placeholder': 'e.g. Honda'}),
            'model':            forms.TextInput(attrs={'placeholder': 'e.g. City'}),
            'year':             forms.NumberInput(attrs={'placeholder': 'e.g. 2022'}),
            'price':            forms.NumberInput(attrs={'placeholder': 'e.g. 950000'}),
            'km_driven':        forms.NumberInput(attrs={'placeholder': 'e.g. 25000'}),
            'color':            forms.TextInput(attrs={'placeholder': 'e.g. White'}),
            'mileage':          forms.NumberInput(attrs={'placeholder': 'e.g. 17.5'}),
            'engine_cc':        forms.NumberInput(attrs={'placeholder': 'e.g. 1497'}),
            'seating_capacity': forms.NumberInput(attrs={'placeholder': 'e.g. 5'}),
            'city':             forms.TextInput(attrs={'placeholder': 'e.g. Ahmedabad'}),
            'description':      forms.Textarea(attrs={'placeholder': 'Describe your car...', 'rows': 4}),
        }


class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image_url', 'caption']
        widgets = {
            'image_url': forms.URLInput(attrs={'placeholder': 'Paste image URL here'}),
            'caption':   forms.TextInput(attrs={'placeholder': 'e.g. Front View'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'MobileNo',
            'gender','profile_picture'
        ]
        widgets = {
            'first_name':       forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name':        forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'MobileNo':         forms.NumberInput(attrs={'placeholder': 'Enter mobile number'}),
        }