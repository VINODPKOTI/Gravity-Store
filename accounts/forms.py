from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Address
INPUT_CLASS = (
    "flex h-10 w-full  border border-zinc-200 bg-white px-3 py-2 text-sm "
    "ring-offset-white placeholder:text-zinc-500 "
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-2 "
    "disabled:cursor-not-allowed disabled:opacity-50 "
)

TEXTAREA_CLASS = (
    "flex min-h-[80px] w-full  border border-zinc-200 bg-white px-3 py-2 text-sm "
    "ring-offset-white placeholder:text-zinc-500 "
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-2 "
    "disabled:cursor-not-allowed disabled:opacity-50"
)



class RegistrationForm(UserCreationForm):
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS})
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone")

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": INPUT_CLASS}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": INPUT_CLASS}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": INPUT_CLASS}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone")


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "full_name", "phone_number", "street_address", "road", "house_number",
            "village", "county", "city", "state_district", "state",
            "postal_code", "country", "latitude", "longitude", "is_default"
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "phone_number": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "street_address": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3}),
            "road": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "house_number": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "village": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "county": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "city": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "state_district": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "state": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "postal_code": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "country": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "latitude": forms.TextInput(attrs={"class": INPUT_CLASS, "readonly": True}),
            "longitude": forms.TextInput(attrs={"class": INPUT_CLASS, "readonly": True}),
            "is_default": forms.CheckboxInput(attrs={
                "class": "h-4 w-4 rounded border-zinc-300 text-zinc-900 focus:ring-zinc-950"
            }),
        }
