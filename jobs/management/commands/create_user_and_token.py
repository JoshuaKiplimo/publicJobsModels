# myapp/management/commands/create_user_and_token.py
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create a user and obtain a token for the user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username for the new user')
        parser.add_argument('password', type=str, help='The password for the new user')

    def handle(self, *args, **options):
        # Retrieve username and password from command line arguments
        username = options['username']
        password = options['password']

        # Create a new user
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        # Obtain or create a token for the user
        token, created = Token.objects.get_or_create(user=user)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'There is something wrong!'))
            
            
