from django.core.management import BaseCommand
from django.db import models

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
# Show this when the user types help
    help = "My test command"
    print help

# A command must define handle()
    def handle(self, *args, **options):
        self.stdout.write("Doing All The Things!")
        from trips.models import Price
        Price.objects.create(name='thbbk', price='1123')

	def biance():
		from trips.models import Price
		#Price.objects.create(name='teeeeeee', price='1123')
		self.stdout.write("Doing All The Things!")
        Price.objects.create(name='binance', price='1123')
