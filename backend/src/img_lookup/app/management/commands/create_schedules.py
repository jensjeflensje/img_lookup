from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    help = "Create task schedules"

    def handle(self, *args, **options):
        schedule('img_lookup.app.tasks.clean_up_assets',
                 schedule_type=Schedule.CRON,
                 cron='0/5 * * * *')