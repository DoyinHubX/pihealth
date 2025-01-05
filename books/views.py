from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q # For complex lookups
from django.urls import reverse_lazy

from .models import Book, Review, Category, CustomUser
from .forms import ReviewForm, CategoryForm, CustomUserCreationForm, CustomUserUpdateForm, CustomUserChangeForm, BookForm

from django.db.models import Q

# Check if the user is staff
def is_admin(user):
    return user.is_staff


# Home Page
class HomePageView(TemplateView):
    template_name = 'books/index.html'


#Auth Section
#------------------------------------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'books/registration/login.html'

# class RegisterView(TemplateView):
#     template_name = 'books/registration/register.html'

#     def post(self, request, *args, **kwargs):
#         # Get form data from POST request
#         username = request.POST.get('registration-username')
#         email = request.POST.get('registration-email')
#         password1 = request.POST.get('registration-password1')
#         password2 = request.POST.get('registration-password2')

#         # Basic validations
#         if not username or not email:
#             messages.error(request, "All fields are required.")
#             return self.render_to_response(self.get_context_data())

#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return self.render_to_response(self.get_context_data())

#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username is already taken.")
#             return self.render_to_response(self.get_context_data())

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "Email is already registered.")
#             return self.render_to_response(self.get_context_data())

#         # Encrypt password before saving
#         hashed_password = make_password(password1)

#         # Create the user
#         user = CustomUser.objects.create_user(username=username, email=email, password=hashed_password)
#         user.save()

#         # Log the user in and redirect
#         login(request, user)
#         messages.success(request, "Registration successful. Welcome!")
#         return redirect('book-list')


class RegisterView(TemplateView):
    template_name = 'books/registration/register.html'

    def post(self, request, *args, **kwargs):
        # Get form data from POST request
        username = request.POST.get('registration-username')
        email = request.POST.get('registration-email')
        password1 = request.POST.get('registration-password1')
        password2 = request.POST.get('registration-password2')

        # Basic validations
        if not username or not email:
            messages.error(request, "All fields are required.")
            return self.render_to_response(self.get_context_data())

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return self.render_to_response(self.get_context_data())

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return self.render_to_response(self.get_context_data())

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return self.render_to_response(self.get_context_data())

        # Create the user
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Log the user in and redirect
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect('predict_risk')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return self.render_to_response(self.get_context_data())


#Book Categories 
#------------------------------------------------------------------------------
@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'books/categories/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'books/categories/category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
@user_passes_test(is_admin)
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'books/categories/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category-list')
    return render(request, 'books/categories/category_confirm_delete.html', {'category': category})


#Book Management
#------------------------------------------------------------------------------
class BookListView(ListView):
    model = Book
    template_name = 'books/partials/book_list.html'
    context_object_name = 'books'
    paginate_by = 10  # Adjust as needed

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Get the search query from the URL
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query) | 
                Q(genre__name__icontains=query)  # Use genre__name to filter by the related Category's name
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')  # Pass the search query to the template
        return context


# Book Detail
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/partials/book_detail.html'


# Book Create
class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/partials/book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Allow access to superusers and users in the 'Manager' group
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to create books.")
        return redirect('book-list')

    def form_valid(self, form):
        messages.success(self.request, "Book has been created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create book. Please correct the errors.")
        return super().form_invalid(form)


# Book Update
class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/partials/book_form.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Allow superusers and users in the 'Manager' group to edit books
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to edit books.")
        return redirect('book-list')

    def form_valid(self, form):
        messages.success(self.request, "Book details have been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update book. Please correct the errors.")
        return super().form_invalid(form)


# Book Delete
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/partials/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

    def test_func(self):
        # Allow only superusers to delete books
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete books.")
        return redirect('book-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Book has been deleted successfully.")
        return super().delete(request, *args, **kwargs)


# Book Review
#------------------------------------------------------------------------------
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the review user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs['pk'])  # Link to the book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('book-detail', kwargs={'pk': self.kwargs['pk']})

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/partials/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()  # Fetch reviews for the book
        context['review_form'] = ReviewForm()  # Include review form
        return context


# Dashboard
#------------------------------------------------------------------------------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'books/registration/dashboard.html'

# User Profile Update
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'books/registration/profile_update.html'
    success_url = reverse_lazy('book-list')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to update profile. Please try again.")
        return super().form_invalid(form)


# User Management
#------------------------------------------------------------------------------
@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'books/users/user_list.html', {'users': users})

# Create User
@login_required
def user_create(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('user-list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/users/user_form.html', {'form': form, 'title': 'Create User'})

# Update User
@login_required
def user_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('user-list')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'books/users/user_form.html', {'form': form, 'title': 'Update User'})

# Delete User
@login_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully!")
        return redirect('user-list')
    return render(request, 'books/users/user_confirm_delete.html', {'user': user})
