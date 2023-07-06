from django.core.management.base import BaseCommand

from authentication.models import AdminPage
from control_panel.urls import urlpatterns


class Command(BaseCommand):
    help = 'For each url in control_panel, create AdminPage object with url name'

    def handle(self, *args, **options):
        all_names = set(x.name for x in urlpatterns if getattr(x, 'name', None))
        registered_names = set(AdminPage.objects.values_list('name', flat=True).distinct())

        new_names = all_names - registered_names

        self.stdout.write(
            f'{len(new_names)} new url names found. Registering.'
        )

        new_pages = [AdminPage(name=x) for x in new_names]
        AdminPage.objects.bulk_create(new_pages)

        self.stdout.write(
            self.style.SUCCESS("AdminPages created successfully")
        )
