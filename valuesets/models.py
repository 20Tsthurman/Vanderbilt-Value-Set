from django.db import models

class Medication(models.Model):
    medication_id = models.IntegerField(primary_key=True)
    medname = models.CharField(max_length=255)
    simple_generic_name = models.CharField(max_length=255)
    route = models.CharField(max_length=50)
    outpatients = models.IntegerField()
    inpatients = models.IntegerField()
    patients = models.IntegerField()

    def __str__(self):
        return self.medname

class ValueSet(models.Model):
    value_set_id = models.IntegerField(primary_key=True)
    value_set_name = models.CharField(max_length=255)
    medications = models.ManyToManyField(Medication)

    def __str__(self):
        return self.value_set_name