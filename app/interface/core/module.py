from django.conf import settings

from systems.command.base import command_set
from systems.command.factory import resource
from systems.command.types import module
from systems.command.mixins import db

import time


class InitCommand(
    module.ModuleActionCommand
):
    def exec(self):
        def run():
            self._module.ensure(self, True)

        self.run_exclusive('module-init', run)


class InstallCommand(
    module.ModuleActionCommand
):
    def exec(self):
        self.info("Installing module requirements...")
        self.manager.install_scripts(self, self.verbosity == 3)
        self.manager.install_requirements(self, self.verbosity == 3)

        if settings.CLI_EXEC:
            env = self.get_env()
            cid = self.manager.container_id
            image = self.manager.generate_image_name(env.base_image)

            self.manager.create_image(cid, image)
            env.runtime_image = image
            env.save()

        self.success("Successfully installed module requirements")


class ResetCommand(
    module.ModuleActionCommand
):
    def exec(self):
        env = self.get_env()
        env.runtime_image = None
        env.save()
        self.set_state('module_ensure', True)
        self.success("Successfully reset module runtime")


class SyncCommand(
    db.DatabaseMixin,
    module.ModuleActionCommand
):
    def exec(self):
        self.silent_data('modules', self.db.save('module', encrypted = False))

    def postprocess(self, result):
        self.db.load(result.get_named_data('modules'), encrypted = False)
        for module in self.get_instances(self._module):
            module.provider.update()

        self.exec_local('module install')
        self.success('Modules successfully synced from remote environment')


class Command(module.ModuleRouterCommand):

    def get_subcommands(self):
        return command_set(
            resource.ResourceCommandSet(
                module.ModuleActionCommand, self.name,
                provider_name = self.name
            ),
            ('init', InitCommand),
            ('install', InstallCommand),
            ('reset', ResetCommand),
            ('sync', SyncCommand)
        )
