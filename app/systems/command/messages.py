from django.conf import settings
from django.core.management.color import color_style
from django.utils.module_loading import import_string

from systems.command import mixins
from utility.encryption import Cipher
from utility.display import format_table

import sys
import json
import logging


logger = logging.getLogger(__name__)


class AppMessage(mixins.ColorMixin):

    cipher = Cipher.get('message')

    @classmethod
    def get(cls, data):
        message = cls.cipher.decrypt(data['package'], False)
        data = json.loads(message)

        try:
            msg = import_string(data['type'])
        except Exception:
            msg = getattr(sys.modules[__name__], data['type'])()
        
        msg.load(data)
        return msg
   

    def __init__(self, message = '', name = None, prefix = None, silent = False, colorize = True):
        self.style = color_style()
        self.colorize = colorize

        self.type = self.__class__.__name__
        self.name = name
        self.prefix = prefix
        self.message = message
        self.silent = silent


    def load(self, data):
        for field, value in data.items():
            if field != 'type':
                setattr(self, field, value)


    def render(self):
        data = { 
            'type': self.type, 
            'message': self.message 
        }
        if self.name:
            data['name'] = self.name

        if self.prefix:
            data['prefix'] = self.prefix

        if self.silent:
            data['silent'] = self.silent
        
        return data

    def to_json(self):
        return json.dumps(self.render())

    def to_package(self):
        json_text = self.to_json()
        ciphertext = self.__class__.cipher.encrypt(json_text).decode('utf-8')
        package = json.dumps({ 'package': ciphertext }) + "\n"
        return (package, json_text)


    def format(self):
        return "{}{}".format(self._format_prefix(), self.message)

    def _format_prefix(self):
        if self.prefix:
            return self.warning_color(self.prefix) + ' '
        else:
            return ''
    
    def display(self):
        if not self.silent:
            print(self.format())


class DataMessage(AppMessage):

    def __init__(self, message = '', data = None, name = None, prefix = None, silent = False, colorize = True):
        super().__init__(message, 
            name = name, 
            prefix = prefix, 
            silent = silent,
            colorize = colorize
        )
        self.data = data

    def render(self):
        result = super().render()
        result['data'] = self.data
        return result

    def format(self):
        return "{}{}: {}".format(
            self._format_prefix(),
            self.message, 
            self.success_color(self.data)
        )


class InfoMessage(AppMessage):
    pass


class NoticeMessage(AppMessage):

    def format(self):
        return "{}{}".format(self._format_prefix(), self.notice_color(self.message))


class SuccessMessage(AppMessage):

    def format(self):
        return "{}{}".format(self._format_prefix(), self.success_color(self.message))


class WarningMessage(AppMessage):

    def format(self):
        return "{}{}".format(self._format_prefix(), self.warning_color(self.message))


class ErrorMessage(AppMessage):

    def __init__(self, message = '', traceback = None, name = None, prefix = None, silent = False, colorize = True):
        super().__init__(message, 
            name = name, 
            prefix = prefix, 
            silent = silent,
            colorize = colorize
        )
        self.traceback = traceback

    def render(self):
        result = super().render()
        result['traceback'] = self.traceback
        return result

    def format(self):
        if settings.DEBUG:
            traceback = [ item.strip() for item in self.traceback ]
            return "\n{}** {}\n\n> {}\n".format(
                self._format_prefix(),
                self.error_color(self.message), 
                self.warning_color("\n".join(traceback))
            )
        return "{}** {}".format(self._format_prefix(), self.error_color(self.message))


class TableMessage(AppMessage):

    def format(self):
        return "\n" + format_table(self.message, self._format_prefix())
