from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patients_list, name='patients_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('visits/new/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visits/<int:pk>/edit/', views.visit_edit, name='visit_edit'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/complete/', views.appointment_complete, name='appointment_complete'),
    path('exercises/', views.exercises_list, name='exercises_list'),
    path('pending-payments/', views.pending_payments, name='pending_payments'),
    path('settings/', views.settings_view, name='settings'),
]

