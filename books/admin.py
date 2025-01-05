from django.contrib import admin
from .models import CustomUser, Book, Review, Category
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('profile_pic',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('profile_pic',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'isbn', 'summary', 'published_date', 'cover_image')
    search_fields = ('title', 'author', 'genre')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Category, CategoryAdmin)
