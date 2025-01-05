from django.urls import path
from . import views
from .views import radar_chart_for_patient

urlpatterns = [
    path('predict/', views.predict_risk, name='predict_risk'),
    path('bulk-prediction/', views.bulk_prediction, name='bulk_prediction'),
]


urlpatterns += [
    path('records/', views.list_records, name='list_records'),
    path('records/create/', views.create_record, name='create_record'),
    path('records/update/<int:pk>/', views.update_record, name='update_record'),
    path('records/delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('bulk_upload/', views.bulk_upload, name='bulk_upload'),
    path('chd-dashboard/', views.chd_dashboard, name='chd_dashboard'),
    path('patient/<int:patient_id>/radar-chart/', radar_chart_for_patient, name='radar_chart_for_patient'),
]



