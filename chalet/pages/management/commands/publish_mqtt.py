from django.core.management.base import BaseCommand
from chalet.mqtt_client import publish_message

class Command(BaseCommand):
    help = 'Envoie un message MQTT'

    def add_arguments(self, parser):
        parser.add_argument('message', type=str, help='Message à envoyer')

    def handle(self, *args, **kwargs):
        message = kwargs['message']
        publish_message(message)