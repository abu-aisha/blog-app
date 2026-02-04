from django.db import models
from django.contrib.auth.models import Group

# Create your models here.



class GroupHierarchy(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )
    level = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Group hierarchies'

    def __str__(self):
        return self.group.name
    

