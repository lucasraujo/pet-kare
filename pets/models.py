from django.db import models


class SexOfPet(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NOTIMFORMED = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()

    sex = models.CharField(
        max_length=20, choices=SexOfPet.choices, default=SexOfPet.NOTIMFORMED
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )
    
    traits = models.ManyToManyField(
        "traits.Trait", related_name="pets"
    )