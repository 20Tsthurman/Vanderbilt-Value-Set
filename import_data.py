import csv
from valuesets.models import ValueSet, Medication

def run():
    # Import medications
    with open('data/medications.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            medication = Medication(
                medication_id=row['medication_id'],
                medname=row['medname'],
                simple_generic_name=row['simple_generic_name'],
                route=row['route'],
                outpatients=row['outpatients'],
                inpatients=row['inpatients'],
                patients=row['patients']
            )
            medication.save()

    # Import value sets
    with open('data/beta_blocker_value_sets.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value_set = ValueSet(
                value_set_id=row['value_set_id'],
                value_set_name=row['value_set_name']
            )
            value_set.save()
            medication_ids = row['medications'].split('|')
            medications = Medication.objects.filter(medication_id__in=medication_ids)
            value_set.medications.set(medications)

if __name__ == '__main__':
    run()