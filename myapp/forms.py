from django import forms
from .models import Service, Review
from .models import empdata

class EmpDataForm(forms.ModelForm):
    class Meta:
        model = empdata
        fields = ['name', 'email', 'password', 'address', 'contact_no', 'location']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'service_type', 'description', 'address', 'contact_no']

        widgets = {
            'name': forms.TextInput(attrs={'required': True, 'minlength': 3,'placeholder': 'Enter Name'}),
            'service_type': forms.Select(attrs={'required': True}),
            'description': forms.Textarea(attrs={'required': True, 'rows': 3}),
            'address': forms.TextInput(attrs={'required': True, 'placeholder': 'Enter address'}),
            'contact_no': forms.TextInput(attrs={'required': True, 'placeholder': 'Enter contact number'}),
        }

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address or address.strip() == "":
            raise forms.ValidationError("Address is required.")
        return address

    def clean_contact_no(self):
        contact = self.cleaned_data.get('contact_no')
        if not contact:
            raise forms.ValidationError("Contact number is required.")
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must be digits only.")
        if len(contact) < 10:
            raise forms.ValidationError("Contact number must be at least 10 digits.")
        if len(contact) != 10:
           raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write your review...'}),
        }
