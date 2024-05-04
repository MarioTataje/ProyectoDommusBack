from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)

    def str(self):
        return self.name

    class Meta:
        db_table = 'universities'


class Degree(models.Model):
    name = models.CharField(max_length=255)
    universities = models.ManyToManyField(University, related_name='universities')

    def str(self):
        return self.name

    class Meta:
        db_table = 'degrees'
