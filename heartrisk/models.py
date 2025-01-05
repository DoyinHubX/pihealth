from django.db import models
from django.db import models

class PatientData(models.Model):
    GENDER_CHOICES = [
        (1, 'Male'),
        (0, 'Female'),
    ]

    EDUCATION_CHOICES = [
        (1, 'Some High School'),
        (2, 'High School Graduate'),
        (3, 'Some College'),
        (4, 'College Graduate'),
    ]

    male = models.IntegerField(choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    education = models.IntegerField(choices=EDUCATION_CHOICES)
    current_smoker = models.BooleanField()
    cigs_per_day = models.FloatField(null=True, blank=True)
    bp_meds = models.BooleanField()
    prevalent_stroke = models.BooleanField()
    prevalent_hyp = models.BooleanField()
    diabetes = models.BooleanField()
    tot_chol = models.FloatField()
    sys_bp = models.FloatField()
    dia_bp = models.FloatField()
    bmi = models.FloatField()
    heart_rate = models.PositiveIntegerField()
    glucose = models.FloatField()
    ten_year_chd = models.BooleanField(default=False)  # Prediction field

    def __str__(self):
        return f"Patient {self.id} - Age: {self.age}, Gender: {'Male' if self.male == 1 else 'Female'}"

class CHDRecord(models.Model):
    male = models.BooleanField(default=False)
    age = models.PositiveIntegerField()
    education = models.PositiveIntegerField()
    current_smoker = models.BooleanField(default=False)
    cigs_per_day = models.PositiveIntegerField(default=0)
    bp_meds = models.BooleanField(default=False)
    prevalent_stroke = models.BooleanField(default=False)
    prevalent_hyp = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    tot_chol = models.FloatField()
    sys_bp = models.FloatField()
    dia_bp = models.FloatField()
    bmi = models.FloatField()
    heart_rate = models.FloatField()
    glucose = models.FloatField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, choices=[('At Risk', 'At Risk'), ('Not At Risk', 'Not At Risk')])

    def __str__(self):
        return f"CHD Record (Age: {self.age}, Risk: {self.risk_level})"

    def clean(self):
        if self.glucose is not None and not isinstance(self.glucose, float):
            raise ValidationError({'glucose': 'Glucose must be a valid number or left blank.'})
