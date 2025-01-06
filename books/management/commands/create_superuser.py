from django.core.management.base import BaseCommand
from books.models import CustomUser

class Command(BaseCommand):
    help = 'Creates a superuser automatically'

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(email='intelliport').exists():
            CustomUser.objects.create_superuser(
                username='intelliport',
                email='intelliport@gmail.com',
                password='intelliport'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))