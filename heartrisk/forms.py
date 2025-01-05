from django import forms
from .models import CHDRecord

class CHDPredictionForm(forms.Form):
    male = forms.ChoiceField(
        label='Gender', 
        choices=[(1, 'Male'), (0, 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        label='Age', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    education = forms.ChoiceField(
        label='Education Level', 
        choices=[(1, 'Some High School'), 
                 (2, 'High School Graduate'), 
                 (3, 'Some College'), 
                 (4, 'College Graduate')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    current_smoker = forms.ChoiceField(
        label='Current Smoker', 
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cigs_per_day = forms.FloatField(
        label='Cigarettes Per Day', 
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bp_meds = forms.ChoiceField(
        label='Blood Pressure Medication', 
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prevalent_stroke = forms.ChoiceField(
        label='History of Stroke', 
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prevalent_hyp = forms.ChoiceField(
        label='History of Hypertension', 
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    diabetes = forms.ChoiceField(
        label='Diabetes', 
        choices=[(1, 'Yes'), (0, 'No')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tot_chol = forms.FloatField(
        label='Total Cholesterol', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sys_bp = forms.FloatField(
        label='Systolic Blood Pressure', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    dia_bp = forms.FloatField(
        label='Diastolic Blood Pressure', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bmi = forms.FloatField(
        label='BMI (Body Mass Index)', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    heart_rate = forms.IntegerField(
        label='Heart Rate', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    glucose = forms.FloatField(
        label='Glucose Level', 
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class BulkPredictionForm(forms.Form):
    file = forms.FileField(label="Upload CSV/Excel File", required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))


# Model form for managing CHD records
class CHDRecordForm(forms.ModelForm):
    class Meta:
        model = CHDRecord
        fields = [
            'male', 'age', 'education', 'current_smoker', 'cigs_per_day', 
            'bp_meds', 'prevalent_stroke', 'prevalent_hyp', 'diabetes',
            'tot_chol', 'sys_bp', 'dia_bp', 'bmi', 'heart_rate', 'glucose', 'risk_level'
        ]
        widgets = {
            'male': forms.Select(choices=[(1, '1 - Male'), (0, '0 - Female')], attrs={'class': 'form-control'}),
            'education': forms.Select(choices=[
                (1, '1 - Some High School'), 
                (2, '2 - High School Graduate'), 
                (3, '3 - Some College'), 
                (4, '4 - College Graduate')
            ], attrs={'class': 'form-control'}),
            'current_smoker': forms.Select(choices=[(1, '1 - Yes'), (0, '0 - No')], attrs={'class': 'form-control'}),
            'bp_meds': forms.Select(choices=[(1, '1 - Yes'), (0, '0 - No')], attrs={'class': 'form-control'}),
            'prevalent_stroke': forms.Select(choices=[(1, '1 - Yes'), (0, '0 - No')], attrs={'class': 'form-control'}),
            'prevalent_hyp': forms.Select(choices=[(1, '1 - Yes'), (0, '0 - No')], attrs={'class': 'form-control'}),
            'diabetes': forms.Select(choices=[(1, '1 - Yes'), (0, '0 - No')], attrs={'class': 'form-control'}),
            'risk_level': forms.Select(choices=[
                ('At Risk', 'At Risk'), 
                ('Not At Risk', 'Not At Risk')
            ], attrs={'class': 'form-control'}),
        }