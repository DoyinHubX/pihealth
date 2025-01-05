from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Book, Review, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter category description'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_pic']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_pic', 
            'first_name', 
            'last_name', 
            'age', 
            'gender', 
            'education', 
            'weight', 
            'height', 
            'heart_rate', 
            'blood_pressure', 
            'bmi', 
            'glucose_level'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'education': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in kg'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height in meters'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Heart rate in bpm'}),
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 120/80'}),
            'bmi': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Body Mass Index'}),
            'glucose_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Glucose level in mg/dL'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'isbn', 'summary', 'published_date', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),  # Use Select for genre to create a dropdown
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'form-check-inline'}),  # Add Bootstrap inline class
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

