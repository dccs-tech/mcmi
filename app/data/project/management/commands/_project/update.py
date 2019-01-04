from systems.command import types, mixins


class UpdateCommand(
    mixins.op.UpdateMixin,
    mixins.data.ProjectMixin, 
    types.ProjectActionCommand
):
    def get_description(self, overview):
        if overview:
            return """update existing projects in current environment

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam 
pulvinar nisl ac magna ultricies dignissim. Praesent eu feugiat 
elit. Cras porta magna vel blandit euismod.
"""
        else:
            return """update existing projects in current environment
                      
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
        self.parse_project_reference()
        self.parse_project_fields(True)

    def exec(self):
        def update_project(project, state):
            project.project_provider.update_project(self.project_fields)
            self.exec_update(
                self._project, 
                project.name, 
                self.project_fields
            )
        self.run_list(self.projects, update_project)
