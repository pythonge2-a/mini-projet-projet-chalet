from django.core.management.base import BaseCommand
from chalet.mqtt_client import print_connected_clients

class Command(BaseCommand):
    help = 'Liste les appareils MQTT connectés'

    def handle(self, *args, **kwargs):
        print_connected_clients()