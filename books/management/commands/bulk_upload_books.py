# books/management/commands/bulk_upload_books.py
from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date

class Command(BaseCommand):
    help = 'Bulk upload books into the database'

    def handle(self, *args, **kwargs):
        # Sample data
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'genre': 'Fiction',
                'isbn': '9780743273565',
                'summary': 'A story of the mysterious Jay Gatsby and his obsession with Daisy Buchanan.',
                'published_date': date(1925, 4, 10),
                'cover_image': 'gatsby.jpeg',  # This should match the actual image file name
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'genre': 'Fiction',
                'isbn': '9780061120084',
                'summary': 'A coming-of-age story that explores themes of racial injustice in the South.',
                'published_date': date(1960, 7, 11),
                'cover_image': '',
            },
            # Add all the other books here...
        ]

        # Create Book objects
        books = [Book(**book) for book in books_data]

        # Bulk create the books in the database
        Book.objects.bulk_create(books)

        self.stdout.write(self.style.SUCCESS('Successfully uploaded books!'))
