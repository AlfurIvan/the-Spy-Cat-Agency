from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Mission(models.Model):
    cat = models.OneToOneField("SpyCat", null=True, blank=True, on_delete=models.SET_NULL, related_name="mission")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.cat} ({'Completed' if self.is_completed else 'Ongoing'})"


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return f"Target {self.name} ({'Completed' if self.is_completed else 'Ongoing'})"


class SpyCat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveSmallIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.name
