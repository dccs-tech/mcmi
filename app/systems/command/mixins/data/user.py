from data.user.models import User
from . import DataMixin


class UserMixin(DataMixin):

    schema = {
        'user': {
            'facade': User,
            'provider': True,                       
            'system_fields': (
                'type',
                'config',
                'variables',
                'state_config',
                'created', 
                'updated',
                'last_login'
            )
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.facade_index['00_user'] = self._user
