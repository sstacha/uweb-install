from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = "\n"
    help += "usage: ./manage.py secret_key [option]\n"
    help += "--------------------------------------\n"
    help += "example: ./manage.py secret_key generate\n"
    help += "example: ./manage.py secret_key get\n"
    help += "example: ./manage.py secret_key set [key]\n"
    help += "\n"
    help += "options\n"
    help += "--------\n"
    help += "generate - generates a new secret key and prints it to the screen\n"
    help += "get - prints the current .secret_key file value\n"
    help += "set - sets the .secret_key file value and prints it to the screen\n"
    help += "\n"

    def add_arguments(self, parser):
        parser.add_argument('option', nargs='+', type=str)

    def generate_secret(self, *args, **options):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return get_random_string(50, chars)
        # self.stdout.write(self.style.SUCCESS('SECRET KEY: "%s"' % get_random_string(50, chars)))

    def get_secret(self, *args, **options):
        with open('.secret_key') as file:
            # print the current value
            print ('SECRET_KEY=%s' % file.read())

    def set_secret(self, *args, **options):
        with open('.secret_key', 'w') as file:
            # generate a new secret key
            secret_key = self.generate_secret()
            # write a new generated value to the file
            file.write(secret_key)
            # print the current value
            print('SECRET_KEY=%s' % file.read())

    def handle(self, *args, **options):
        # self.stdout.write(self.style.SUCCESS("subcommand: " + str(options['subcommand'])))
        # self.stdout.write(self.style.SUCCESS("options: " + str(options)))
        if "generate" in options['option']:
            self.stdout.write(self.style.SUCCESS('%s' % self.generate_secret()))
        elif "get" in options['option']:
            self.stdout.write(self.style.SUCCESS('%s' % self.get_secret()))
        elif "set" in options['option']:
            self.stdout.write(self.style.SUCCESS('%s' % self.set_secret()))
        else:
            self.stdout.write(self.style.SUCCESS(self.help))