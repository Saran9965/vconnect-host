from django import forms
from .models import Service
from django import forms
from .models import Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'service_type', 'description', 'address', 'contact_no']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'placeholder': 'Write your review...'}),
        }
