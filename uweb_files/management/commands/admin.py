from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Administrative Commands'

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
        if "generate_secret" in options['option']:
            self.stdout.write(self.style.SUCCESS('%s' % self.generate_secret()))
        else:
            self.stdout.write(self.style.SUCCESS(" "))
            self.stdout.write(self.style.SUCCESS("usage: ./manage.py admin [option]"))
            self.stdout.write(self.style.SUCCESS("example: ./manage.py admin get_secret"))
            self.stdout.write(self.style.SUCCESS("example: ./manage.py admin set_secret [key]"))
            self.stdout.write(self.style.SUCCESS("example: ./manage.py admin generate_secret"))
            self.stdout.write(self.style.SUCCESS(" "))
            self.stdout.write(self.style.SUCCESS("options "))
            self.stdout.write(self.style.SUCCESS("--------"))
            self.stdout.write(self.style.SUCCESS("generate_secret - generates a new secret key and prints it to the screen"))
            self.stdout.write(self.style.SUCCESS("get_secret - prints the current .secret_key value"))
            self.stdout.write(self.style.SUCCESS("set_secret - sets the .secret_key value and prints it to the screen"))
            self.stdout.write(self.style.SUCCESS(" "))
