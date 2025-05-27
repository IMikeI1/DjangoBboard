from django import forms
from django.contrib.auth.models import User
from .models import Bboard

class BboardForm(forms.ModelForm):
    class Meta:
        model = Bboard
        fields = ['title', 'content', 'image', 'year', 'mileage', 'condition',
                  'modification', 'engine_volume', 'engine_type', 'transmission', 'drive',
                  'equipment', 'body_type', 'color', 'steering_wheel', 'price', 'price_arenda_car']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'modification': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_volume': forms.TextInput(attrs={'class': 'form-control'}),
            'engine_type': forms.TextInput(attrs={'class': 'form-control'}),
            'transmission': forms.TextInput(attrs={'class': 'form-control'}),
            'drive': forms.TextInput(attrs={'class': 'form-control'}),
            'equipment': forms.TextInput(attrs={'class': 'form-control'}),
            'body_type': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'steering_wheel': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_arenda_car': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance 
    
    
    
    
class FilterForm(forms.Form):
    author = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Автор')
    created_at = forms.DateField(label='Дата публикации', 
                                 widget=forms.DateInput(attrs={'type':'date'}),
                                 input_formats=['%Y-%m-%d'],
                                 required=False)
