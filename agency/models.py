import requests
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        # Validate breed using TheCatAPI
        url = "https://api.thecatapi.com/v1/breeds"
        response = requests.get(url, headers={"x-api-key": settings.CAT_API_KEY})
        print(response, response.status_code, response.json())
        if response.status_code != 200:
            raise ValidationError("Unable to validate breed due to an API error.")

        breeds = [breed["name"] for breed in response.json()]

        if self.breed not in breeds:
            raise ValidationError(f"Breed '{self.breed}' is not recognized.")

    def __str__(self):
        return self.name

class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, null=True, blank=True, on_delete=models.SET_NULL, related_name="mission")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id} ({'Completed' if self.is_completed else 'Ongoing'})"

class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # prevent updates to notes if target is completed
        if self.pk and self.is_completed:
            old_instance = Target.objects.get(pk=self.pk)
            if old_instance.notes != self.notes:
                raise ValidationError("Cannot update notes on a completed target.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Target {self.name} ({'Completed' if self.is_completed else 'Ongoing'})"
