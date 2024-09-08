from django.core.management.base import BaseCommand
from django.db import transaction
from app import settings
from user.models import User


class Command(BaseCommand):
    help = "Create default data for models"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.HTTP_INFO("Creating superuser..."))
            User.objects.create_superuser(
                **settings.ADMIN_INFO,
            )
            self.stdout.write(self.style.SUCCESS("Created superuser"))
