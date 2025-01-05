from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]

    EDUCATION_CHOICES = [
        (1, 'Some High School'),
        (2, 'High School Graduate'),
        (3, 'Some College'),
        (4, 'College Graduate'),
    ]

    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)  
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)  
    education = models.IntegerField(choices=EDUCATION_CHOICES, null=True, blank=True)  
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Weight in kg
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Height in meters
    heart_rate = models.PositiveIntegerField(null=True, blank=True)  # Heart rate in beats per minute
    blood_pressure = models.CharField(max_length=7, null=True, blank=True)  # BP in '120/80' format
    bmi = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # Body Mass Index
    glucose_level = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Blood glucose level in mg/dL

    def __str__(self):
        return self.username

    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Enter the category/genre name")
    description = models.TextField(blank=True, null=True, help_text="Enter a brief description of the category")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the book title")
    author = models.CharField(max_length=200, help_text="Enter the book author")
    genre = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="Select the book genre")
    isbn = models.CharField(max_length=13, unique=True, help_text="Enter the 13-character ISBN")
    summary = models.TextField(help_text="Enter a brief description of the book")
    published_date = models.DateField(help_text="Enter the published date in YYYY-MM-DD")
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        help_text="Upload a cover image for the book."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(help_text="Enter a rating between 1 and 5")
    comment = models.TextField(help_text="Enter your review", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title} ({self.rating}/5)"
