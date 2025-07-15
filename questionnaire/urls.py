# questionnaire/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register_assessor, name='register_assessor'),
    path('approve/<uuid:token>/', views.approve_assessor, name='approve_assessor'),
    path('decline/<uuid:token>/', views.decline_assessor, name='decline_assessor'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('assessor-dashboard/', views.assessor_dashboard, name='assessor_dashboard'),
    path('dynamic-survey/', views.dynamic_survey, name='dynamic_survey'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('create-survey/', views.create_survey, name='create_survey'),
    path('add-questions/<int:survey_id>/', views.add_questions, name='add_questions'),
    path('remove-question/<int:question_id>/', views.remove_question, name='remove_question'),
    path('review/<int:response_id>/', views.review_survey, name='review_survey'),
    path('review-questions/<int:survey_id>/', views.review_questions, name='review_questions'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('survey/<int:survey_id>/edit/', views.edit_survey, name='edit_survey'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
    path('delete-survey/<int:survey_id>/', views.delete_survey, name='delete_survey'),
    path('responses/', views.response_list, name='response_list'),
    path('responses/<int:response_id>/', views.response_detail, name='response_detail'),
    path('export-all/<int:survey_id>/', views.export_all_responses, name='export_all_responses'),
    path('responses/<int:survey_id>/', views.response_list, name='response_list'),
    path('ml-model-runner/', views.run_ml, name='ml_model_runner'),




]
