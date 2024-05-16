from django.db import models

class Medication(models.Model):
   # Unique identifier for the medication
   medication_id = models.IntegerField(primary_key=True)
   # Name of the medication
   medname = models.CharField(max_length=255)
   # Simplified generic name of the medication
   simple_generic_name = models.CharField(max_length=255)
   # Route of administration for the medication
   route = models.CharField(max_length=50)
   # Number of outpatients prescribed the medication
   outpatients = models.IntegerField()
   # Number of inpatients prescribed the medication
   inpatients = models.IntegerField()
   # Total number of patients prescribed the medication
   patients = models.IntegerField()

   def __str__(self):
       # String representation of the medication
       return self.medname

class ValueSet(models.Model):
   # Unique identifier for the value set
   value_set_id = models.IntegerField(primary_key=True)
   # Name of the value set
   value_set_name = models.CharField(max_length=255)
   # Many-to-many relationship with medications
   medications = models.ManyToManyField(Medication)

   def __str__(self):
       # String representation of the value set
       return self.value_set_name