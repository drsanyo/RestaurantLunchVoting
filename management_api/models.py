from django.db import models


class MenuField(models.Field):
    def from_db_value(self, value, expression, connection):
        return value.tobytes().decode()

    def to_python(self, value):
        return value


class VwCurrentDayMenu(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    rst_name = models.CharField(max_length=150, blank=True, null=True)
    menu = MenuField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'vw_current_day_menu'
