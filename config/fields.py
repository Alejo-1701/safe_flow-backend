from django.db import models


class IntegerForeignKey(models.ForeignKey):
    def get_internal_type(self):
        return "IntegerField"

    def db_type(self, connection):
        return connection.data_types["IntegerField"]


class FixedCharField(models.CharField):
    def db_type(self, connection):
        return f"character({self.max_length})"
