from django.core.management.base import CommandError
from django.utils.timezone import now

from systems.command import SimpleCommand
from data.environment import models


class SetCommand(SimpleCommand):

    def get_description(self, overview):
        if overview:
            return """set current cluster environment (for all operations)

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam 
pulvinar nisl ac magna ultricies dignissim. Praesent eu feugiat 
elit. Cras porta magna vel blandit euismod.
"""
        else:
            return """set current cluster environment (for all operations)
                      
Etiam mattis iaculis felis eu pharetra. Nulla facilisi. 
Duis placerat pulvinar urna et elementum. Mauris enim risus, 
mattis vel risus quis, imperdiet convallis felis. Donec iaculis 
tristique diam eget rutrum.

Etiam sit amet mollis lacus. Nulla pretium, neque id porta feugiat, 
erat sapien sollicitudin tellus, vel fermentum quam purus non sem. 
Mauris venenatis eleifend nulla, ac facilisis nulla efficitur sed. 
Etiam a ipsum odio. Curabitur magna mi, ornare sit amet nulla at, 
scelerisque tristique leo. Curabitur ut faucibus leo, non tincidunt 
velit. Aenean sit amet consequat mauris.
"""

    def add_arguments(self, parser):
        parser.add_argument('environment', nargs=1, type=str, help="environment name")


    def handle(self, *args, **options):
        env_name = options['environment'][0]
        environments = list(models.Environment.objects.all().values_list('name', flat = True))
        
        print("Setting current environment: {}".format(self.style.SUCCESS(env_name)))

        if env_name not in environments:
            raise CommandError(self.style.ERROR("Environment does not exist"))

        state, created = models.State.objects.get_or_create(
            name = 'environment'
        )
        state.value = env_name
        state.timestamp = now()
        state.save()

        if created:
            print(self.style.SUCCESS("> Successfully created environment state"))
        else:
            print(self.style.SUCCESS("> Successfully updated environment state"))

