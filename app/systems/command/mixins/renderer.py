from collections import OrderedDict

from systems.models.base import AppModel
from utility import data, display
from .base import DataMixin
from .config import ConfigMixin

import datetime


class RendererMixin(ConfigMixin, DataMixin):

    def render(self, facade, fields, queryset):
        fields = list(fields)
        data = [fields]

        for instance in queryset:
            instance = self.get_instance_by_id(facade, instance.id, required = False)
            if instance and (getattr(instance, 'provider_type', None) is None or not instance.provider_type.startswith('sys_')):
                record = []

                for field in fields:
                    display_method = getattr(facade, "get_field_{}_display".format(field), None)
                    value = getattr(instance, field, None)

                    if display_method and callable(display_method):
                        value = display_method(instance, value, True)

                    elif isinstance(value, datetime.datetime):
                        value = localtime(value).strftime("%Y-%m-%d %H:%M:%S %Z")

                    record.append(value)

                data.append(record)

        return data


    def get_default_fields(self, facade):
        info = OrderedDict()
        fields = []
        key = None

        for field in facade.field_instances:
            if field.name == facade.key():
                key = field
            elif field.name != facade.pk:
                fields.append(field)

        info[key.name] = key.verbose_name.title()

        for field in sorted(fields, key = lambda x: x.name):
            if not facade.check_field_related(field):
                info[field.name] = field.verbose_name.title()

        return info

    def get_related_fields(self, facade):
        info = {}
        for field_name, field_info in facade.get_all_relations().items():
            info[field_name] = field_info['label']
        return info

    def get_config_fields(self, facade, config_name):
        default_fields = self.get_default_fields(facade)
        overrides = self.get_config(config_name, None)

        if overrides:
            fields = OrderedDict()
            fields[facade.key()] = default_fields[facade.key()]

            for field_name in data.ensure_list(overrides):
                if field_name == 'id':
                    fields[field_name] = 'ID'
                else:
                    if field_name in default_fields:
                        fields[field_name] = default_fields[field_name]

            return fields
        else:
            return default_fields

    def get_config_relations(self, facade, config_name):
        related_fields = self.get_related_fields(facade)
        overrides = self.get_config(config_name, None)

        if overrides:
            fields = OrderedDict()
            for field_name in data.ensure_list(overrides):
                if field_name in related_fields:
                    fields[field_name] = related_fields[field_name]
            return fields
        else:
            return related_fields

    def get_list_fields(self, facade):
        config_name = "{}_{}_list_fields".format(self.active_user.name, facade.name)
        return self.get_config_fields(facade, config_name)

    def get_list_relations(self, facade):
        config_name = "{}_{}_list_fields".format(self.active_user.name, facade.name)
        return self.get_config_relations(facade, config_name)

    def get_display_fields(self, facade):
        config_name = "{}_{}_display_fields".format(self.active_user.name, facade.name)
        return self.get_config_fields(facade, config_name)

    def get_display_relations(self, facade):
        config_name = "{}_{}_display_fields".format(self.active_user.name, facade.name)
        return self.get_config_relations(facade, config_name)


    def render_list_fields(self, facade):
        fields = []
        labels = []

        for name, label in self.get_list_fields(facade).items():
            fields.append(name)
            labels.append(label)

        return (fields, labels)


    def render_relation_overview(self, facade, name, instances):
        facade = facade.manager.get_facade_index()[name]
        relations = facade.get_all_relations()
        fields, labels = self.render_list_fields(facade)
        field_relations = []

        for name, label in self.get_list_relations(facade).items():
            field_relations.append(name)
            labels.append(label)

        data = self.render(facade, ['id'] + fields,
            facade.filter(**{
                'id__in': instances.keys()
            })
        )
        data[0] = [ self.header_color(x) for x in labels ]
        if len(data) > 1:
            for index, info in enumerate(data[1:]):
                id = info.pop(0)
                for field_name in field_relations:
                    field_info = relations[field_name]
                    items = []
                    value = getattr(instances[id], field_name)

                    if field_info['multiple']:
                        for sub_instance in value.all():
                            items.append(self.relation_color(str(sub_instance)))
                    else:
                        items.append(self.relation_color(str(value)))

                    info.append("\n".join(items))
        else:
            data = []
        return data


    def render_list(self, facade, filters = {}):
        relations = facade.get_all_relations()
        data = []
        fields, labels = self.render_list_fields(facade)
        field_relations = []

        for name, label in self.get_list_relations(facade).items():
            field_relations.append(name)
            labels.append(label)

        if facade.count(**filters):
            data = self.render(facade, ['id'] + fields, facade.filter(**filters))
            id_index = data[0].index(facade.pk)
            key_index = (data[0].index(facade.key()) - 1)

            data[0] = [ self.header_color(x) for x in labels ]

            for index, info in enumerate(data[1:]):
                id = info.pop(id_index)
                instance = self.get_instance_by_id(facade, id, required = False)
                info[key_index] = info[key_index]

                for field_name in field_relations:
                    field_info = relations[field_name]
                    items = []
                    value = getattr(instance, field_name)

                    if field_info['multiple']:
                        for sub_instance in value.all():
                            items.append(self.relation_color(str(sub_instance)))
                    else:
                        items.append(self.relation_color(str(value)))

                    info.append("\n".join(items))

        return data


    def render_display(self, facade, name):
        if isinstance(name, AppModel):
            instance = name
        else:
            instance = self.get_instance(facade, name, required = False)

        relations = facade.get_all_relations()
        data = []

        if instance:
            for name, label in self.get_display_fields(facade).items():
                display_method = getattr(facade, "get_field_{}_display".format(name), None)
                value = getattr(instance, name, None)

                if display_method and callable(display_method):
                    value = display_method(instance, value, False)
                else:
                    if isinstance(value, datetime.datetime):
                        value = localtime(value).strftime("%Y-%m-%d %H:%M:%S %Z")
                    else:
                        value = str(value)

                data.append((
                    self.header_color(label),
                    value
                ))

            data.append((' ', ' '))
            for name, label in self.get_display_relations(facade).items():
                field_info = relations[name]
                label = self.header_color(label)
                value = getattr(instance, name)

                if field_info['multiple']:
                    instances = { x.id: x for x in value.all() }
                    relation_data = self.render_relation_overview(facade, field_info['name'], instances)
                    if relation_data:
                        value = display.format_data(relation_data)
                        data.append((label, value + "\n"))
                else:
                    data.append((label, self.relation_color(str(value)) + "\n"))
        else:
            self.error("{} {} does not exist".format(facade.name.title(), name))

        return data