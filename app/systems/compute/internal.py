from .base import BaseComputeProvider


class Internal(BaseComputeProvider):

    def provider_config(self, type = None):
        self.requirement(str, 'ip', help = 'SSH capable IP of server')
        self.requirement(str, 'password', help = 'Password of server user')

        self.option(str, 'user', 'admin', help = 'Server SSH user', config_name = 'internal_user')
        self.option(str, 'data_device', '/dev/sda4', help = 'Server data drive device', config_name = 'internal_data_device')


    def initialize_instance(self, instance, relations, created):
        if instance.subnet.network.type != 'internal':
            self.command.error("Internally defined network needed to create manual server entries")

        super().initialize_instance(instance, relations, created)