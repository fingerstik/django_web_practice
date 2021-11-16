from django.core.management.base import BaseCommand
from django.utils import timezone
from django_seed import Seed
from jrweb.board.models.post_models import Post


class Command(BaseCommand):
    help = 'Create post what you want'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int, help="How many posts do you want to create?"
        )

    def handle(self, *args, **kwargs):
        number = kwargs.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(Post, number, {
            "title": lambda x: seeder.faker.name(),
            "body": lambda x: seeder.faker.sentence(),
            "date": timezone.now()
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} posts created!'))



