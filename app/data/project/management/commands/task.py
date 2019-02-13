from settings import Roles
from systems.command import types, mixins


class Command(
    mixins.data.ServerMixin, 
    types.ProjectActionCommand
):
    def groups_allowed(self):
        return False # Access control via task definitions

    def get_command_name(self):
        return 'task'

    def get_description(self, overview):
        if overview:
            return """execute a task on existing servers

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam 
pulvinar nisl ac magna ultricies dignissim. Praesent eu feugiat 
elit. Cras porta magna vel blandit euismod.
"""
        else:
            return """execute a task on existing servers
                      
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
    def parse(self):
        self.parse_project_name()
        self.parse_server_reference('--servers')
        self.parse_task_name()        
        self.parse_task_params(True)

    def exec(self):
        self.project.provider.exec_task(
            self.task_name,
            self.servers,
            self.task_params
        )