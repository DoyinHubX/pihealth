from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count

from .forms import CHDPredictionForm, BulkPredictionForm, CHDRecordForm
from .models import PatientData, CHDRecord  # Import your Prediction model

import csv
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Load the model
MODEL_PATH = 'heartrisk/ml_models/framingham_heart_risk_model.pkl'
model = joblib.load(MODEL_PATH)


# Custom decorator for access control
def superuser_or_manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.groups.filter(name='Manager').exists()):
            # Redirect unauthorized users or show an error message
            from django.contrib import messages
            messages.error(request, "You do not have permission to access this page.")
            return redirect('book-list')  # Replace 'home' with your desired redirect view
        return view_func(request, *args, **kwargs)
    return _wrapped_view



#SIngle patient prediction
#----------------------------------------------------------------------------------------
def predict_risk(request):
    if request.method == 'POST':
        form = CHDPredictionForm(request.POST)
        if form.is_valid():
            # Extract form data
            data = {field: float(form.cleaned_data[field]) for field in form.cleaned_data}
            
            # Predict the risk level
            prediction = model.predict([list(data.values())])[0]
            is_at_risk = True if prediction == 1 else False  # Boolean value for ten_year_chd
            
            # Determine the risk level for feedback
            risk_level = "At Risk" if is_at_risk else "Not At Risk"
            
            # Save to the database
            record = PatientData(
                male=data.get('male'),
                age=data.get('age'),
                education=data.get('education'),
                current_smoker=data.get('current_smoker'),
                cigs_per_day=data.get('cigs_per_day'),
                bp_meds=data.get('bp_meds'),
                prevalent_stroke=data.get('prevalent_stroke'),
                prevalent_hyp=data.get('prevalent_hyp'),
                diabetes=data.get('diabetes'),
                tot_chol=data.get('tot_chol'),
                sys_bp=data.get('sys_bp'),
                dia_bp=data.get('dia_bp'),
                bmi=data.get('bmi'),
                heart_rate=data.get('heart_rate'),
                glucose=data.get('glucose'),
                ten_year_chd=is_at_risk  # Save boolean value
            )
            record.save()
            
            # Pass the form data as risk factors to the radar chart
            return render(request, 'heartrisk/result.html', {
                'result': "High Risk" if is_at_risk else "Low Risk",
                'risk_level': risk_level,
                'risk_factors': data  # Include the form data as context
            })
    else:
        form = CHDPredictionForm()
    
    return render(request, 'heartrisk/predict.html', {'form': form})


#Bulk Prediction
#----------------------------------------------------------------------------------------
@superuser_or_manager_required
def bulk_prediction(request):
    if request.method == 'POST':
        form = BulkPredictionForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the file using pandas (CSV or Excel)
                if file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    data = pd.read_excel(file)
                else:
                    return render(request, 'heartrisk/error.html', {'error': 'Unsupported file type'})
                
                # Ensure the data contains all required columns
                required_columns = [
                    'male', 'age', 'education', 'current_smoker', 'cigs_per_day',
                    'bp_meds', 'prevalent_stroke', 'prevalent_hyp', 'diabetes',
                    'tot_chol', 'sys_bp', 'dia_bp', 'bmi', 'heart_rate', 'glucose'
                ]
                if not all(col in data.columns for col in required_columns):
                    return render(request, 'heartrisk/error.html', {'error': 'Missing required columns in the file'})
                
                # Load the pre-trained model
                model = joblib.load(MODEL_PATH)

                # Predict and save to database for each row
                predictions = []
                for _, row in data.iterrows():
                    input_data = [row[col] for col in required_columns]  # Prepare the input data
                    prediction = model.predict([input_data])[0]  # Predict CHD risk for this row
                    
                    # Convert prediction to boolean
                    is_at_risk = True if prediction == 1 else False
                    
                    # Save to the database
                    record = PatientData(
                        male=row['male'],
                        age=row['age'],
                        education=row['education'],
                        current_smoker=row['current_smoker'],
                        cigs_per_day=row['cigs_per_day'],
                        bp_meds=row['bp_meds'],
                        prevalent_stroke=row['prevalent_stroke'],
                        prevalent_hyp=row['prevalent_hyp'],
                        diabetes=row['diabetes'],
                        tot_chol=row['tot_chol'],
                        sys_bp=row['sys_bp'],
                        dia_bp=row['dia_bp'],
                        bmi=row['bmi'],
                        heart_rate=row['heart_rate'],
                        glucose=row['glucose'],
                        ten_year_chd=is_at_risk  # Save the boolean prediction
                    )
                    record.save()

                    # Add prediction result for output
                    predictions.append({
                        'male': row['male'],
                        'age': row['age'],
                        'education': row['education'],
                        'current_smoker': row['current_smoker'],
                        'cigs_per_day': row['cigs_per_day'],
                        'bp_meds': row['bp_meds'],
                        'prevalent_stroke': row['prevalent_stroke'],
                        'prevalent_hyp': row['prevalent_hyp'],
                        'diabetes': row['diabetes'],
                        'tot_chol': row['tot_chol'],
                        'sys_bp': row['sys_bp'],
                        'dia_bp': row['dia_bp'],
                        'bmi': row['bmi'],
                        'heart_rate': row['heart_rate'],
                        'glucose': row['glucose'],
                        'Prediction': "High Risk" if is_at_risk else "Low Risk"
                    })
                
                # Pass the result to the template
                return render(request, 'heartrisk/bulk_result.html', {'result': predictions})
            
            except Exception as e:
                return render(request, 'heartrisk/error.html', {'error': str(e)})
    else:
        form = BulkPredictionForm()
    
    return render(request, 'heartrisk/bulk_upload.html', {'form': form})


#----------------------------------------------------------------------------------------
# Custom permission decorator
def admin_only(user):
    return user.is_superuser or user.groups.filter(name='Manager').exists()


# Ensure only admins can access
@user_passes_test(lambda user: user.is_staff)  # Replace with admin-only test if needed
def list_records(request):
    # Get the search query from the URL
    query = request.GET.get('q', '')
    
    # Get all records
    records = CHDRecord.objects.all()
    
    # Apply search filter if query exists
    if query:
        records = records.filter(
            Q(current_smoker__icontains=query) | 
            Q(risk_level__icontains=query)
        )

    # Set up pagination (adjust number of items per page as needed)
    paginator = Paginator(records, 500)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the template with the filtered and paginated records
    return render(request, 'heartrisk/record_list.html', {
        'records': page_obj,
        'query': query  # Pass the query so it remains in the search box
    })


#----------------------------------------------------------------------------------------
@user_passes_test(admin_only)
def create_record(request):
    if request.method == 'POST':
        form = CHDRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record created successfully!")
            return redirect('list_records')  # Redirect to a list or detail page
        else:
            messages.error(request, "Failed to create the record. Please correct the errors below.")
    else:
        form = CHDRecordForm()
    
    return render(request, 'heartrisk/record_form.html', {'form': form, 'title': 'Create CHD Record'})


#----------------------------------------------------------------------------------------
@user_passes_test(admin_only)
def update_record(request, pk):
    record = get_object_or_404(CHDRecord, pk=pk)
    if request.method == 'POST':
        form = CHDRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('list_records')  # Redirect to a list or detail page
        else:
            messages.error(request, "Failed to update the record. Please correct the errors below.")
    else:
        form = CHDRecordForm(instance=record)
    
    return render(request, 'heartrisk/record_form.html', {'form': form, 'title': 'Update CHD Record'})


#----------------------------------------------------------------------------------------
@user_passes_test(admin_only)
def delete_record(request, pk):
    try:
        record = get_object_or_404(CHDRecord, pk=pk)
        if request.method == 'POST':
            record.delete()
            messages.success(request, "Record deleted successfully!")
            return redirect('list_records')
    except Exception as e:
        messages.error(request, f"An error occurred while trying to delete the record: {str(e)}")
        return redirect('list_records')
    
    return render(request, 'heartrisk/confirm_delete.html', {'record': record})


#----------------------------------------------------------------------------------------
import csv
from django.contrib import messages
from django.shortcuts import redirect
from .models import CHDRecord

def bulk_upload(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('uploadFile')
        
        # Check if the file is a CSV
        if not upload_file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('record_list')

        try:
            # Read and decode the CSV file
            decoded_file = upload_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            
            records_to_create = []
            skipped_rows = 0

            for row in csv_reader:
                try:
                    # Clean and validate fields from CSV
                    glucose = row.get('glucose', '').strip()
                    if glucose in ['NA', '', None]:
                        glucose = None  # Treat missing or 'NA' glucose as None
                    else:
                        glucose = float(glucose)  # Convert glucose to float
                    
                    # Create a record instance with cleaned data
                    record = CHDRecord(
                        male=row.get('male') == '1',
                        age=int(row.get('age', 0)),
                        education=int(row.get('education', 0)),
                        current_smoker=row.get('current_smoker') == '1',
                        cigs_per_day=int(row.get('cigs_per_day', 0)),
                        bp_meds=row.get('bp_meds') == '1',
                        prevalent_stroke=row.get('prevalent_stroke') == '1',
                        prevalent_hyp=row.get('prevalent_hyp') == '1',
                        diabetes=row.get('diabetes') == '1',
                        tot_chol=float(row.get('tot_chol', 0)),
                        sys_bp=float(row.get('sys_bp', 0)),
                        dia_bp=float(row.get('dia_bp', 0)),
                        bmi=float(row.get('bmi', 0)),
                        heart_rate=float(row.get('heart_rate', 0)),
                        glucose=glucose,
                        risk_level=row.get('risk_level', 'Not At Risk')
                    )
                    records_to_create.append(record)

                except (ValueError, TypeError) as e:
                    skipped_rows += 1
                    continue  # Skip invalid rows

            # Bulk create all valid records
            CHDRecord.objects.bulk_create(records_to_create)
            
            success_count = len(records_to_create)
            messages.success(request, f"Successfully uploaded {success_count} records. Skipped {skipped_rows} invalid rows.")
        
        except Exception as e:
            messages.error(request, f"An error occurred during upload: {e}")

    return redirect('list_records')


def get_chart_as_base64():
    """Helper function to convert a Matplotlib plot to base64."""
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()
    return image_base64


#----------------------------------------------------------------------------------------
def chd_dashboard(request):
    # Total Number of Records
    total_records = CHDRecord.objects.count()
    records = CHDRecord.objects.all()

    # Average Age of Patients with CHD 
    avg_age = round(CHDRecord.objects.all().aggregate(Avg('age'))['age__avg'] or 0, 2)

    # Mean Cholesterol Levels (Total Cholesterol, HDL, LDL)
    mean_tot_chol = round(CHDRecord.objects.all().aggregate(Avg('tot_chol'))['tot_chol__avg'] or 0, 2)
    mean_hdl_chol = round(CHDRecord.objects.all().aggregate(Avg('sys_bp'))['sys_bp__avg'] or 0, 2)  # Assuming sys_bp is a proxy for HDL
    mean_ldl_chol = round(CHDRecord.objects.all().aggregate(Avg('dia_bp'))['dia_bp__avg'] or 0, 2)  # Assuming dia_bp is a proxy for LDL

    # Average Blood Pressure (Systolic/Diastolic)
    avg_systolic_bp = round(CHDRecord.objects.all().aggregate(Avg('sys_bp'))['sys_bp__avg'] or 0, 2)
    avg_diastolic_bp = round(CHDRecord.objects.all().aggregate(Avg('dia_bp'))['dia_bp__avg'] or 0, 2)

# Generate charts
    charts = {}

    # 1. Age Distribution of Patients with CHD (Histogram)
    plt.figure(figsize=(6, 4))
    sns.histplot(records.values_list('age', flat=True), kde=True, bins=15)
    plt.title('Age Distribution of Patients with CHD')
    charts['age_distribution'] = get_chart_as_base64()

    # 2. BMI Distribution (Histogram)
    plt.figure(figsize=(6, 4))
    sns.histplot(records.values_list('bmi', flat=True), kde=True, bins=15)
    plt.title('BMI Distribution')
    charts['bmi_distribution'] = get_chart_as_base64()

    # 3. Smoking Status by Risk Level (Stacked Bar Chart)
    smoking_data = records.values('current_smoker', 'risk_level')
    smoking_df = pd.DataFrame(list(smoking_data))
    plt.figure(figsize=(6, 4))
    sns.countplot(x='risk_level', hue='current_smoker', data=smoking_df)
    plt.title('Smoking Status by Risk Level')
    charts['smoking_status'] = get_chart_as_base64()

    # Add more charts similarly...

    #heat Map
    # Generate DataFrame for analysis
    data = pd.DataFrame(list(records.values(
        'age', 'tot_chol', 'sys_bp', 'dia_bp', 'current_smoker', 'risk_level'
    )))

    # Map risk_level to numeric for correlation
    risk_mapping = {'Not At Risk': 0, 'At Risk': 1}
    data['risk_level'] = data['risk_level'].map(risk_mapping)

    # Correlation Matrix
    correlation_matrix = data.corr()

    # Generate Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap='coolwarm',
        fmt='.2f',
        square=True,
        cbar=True,
        linewidths=0.5
    )
    plt.title('Correlation Matrix Between Features')
   
    charts['correlation_heatmap'] = get_chart_as_base64()

    context = {
        'total_records': total_records,
        'avg_age': avg_age,
        'mean_tot_chol': mean_tot_chol,
        'mean_hdl_chol': mean_hdl_chol,
        'mean_ldl_chol': mean_ldl_chol,
        'avg_systolic_bp': avg_systolic_bp,
        'avg_diastolic_bp': avg_diastolic_bp,
        'charts': charts,
    }

    return render(request, 'heartrisk/chd_dashboard.html', context)


#----------------------------------------------------------------------------------------
def radar_chart_for_patient(request, patient_id):
    # Retrieve the specific patient record
    try:
        patient = CHDRecord.objects.get(id=patient_id)
    except CHDRecord.DoesNotExist:
        return HttpResponseNotFound("Patient not found")

    # Define risk factors
    risk_factors = {
        'Age': patient.age,
        'Total Cholesterol': patient.tot_chol,
        'Systolic BP': patient.sys_bp,
        'Diastolic BP': patient.dia_bp,
        'Smoking Status': int(patient.current_smoker),  # Convert to 0/1
        'BMI': patient.bmi,
    }

    # Normalize the data
    max_values = {
        'Age': 100,  # Assume max age is 100
        'Total Cholesterol': 300,  # Based on common cholesterol levels
        'Systolic BP': 200,  # Based on common BP levels
        'Diastolic BP': 120,
        'Smoking Status': 1,  # Binary value
        'BMI': 40,  # Based on typical BMI range
    }
    normalized_values = [
        value / max_values[key] for key, value in risk_factors.items()
    ]

    # Radar Chart Setup
    labels = list(risk_factors.keys())
    values = normalized_values
    values += values[:1]  # Repeat first value to close the radar chart

    # Radar Chart Parameters
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Plot Radar Chart
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(f"Risk Factors for Patient {patient_id}", size=16, color='blue', y=1.1)

    # Save Chart as Base64
    chart_base64 = get_chart_as_base64()

    # Render Template
    return render(request, 'heartrisk/radar_chart.html', {
        'patient': patient,
        'chart_base64': chart_base64,
    })