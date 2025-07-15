# questionnaire/ml_forms.py

from django import forms

class MLModelForm(forms.Form):
    MODEL_CHOICES = [
        ('classification', 'Classification Model (Logistic Regression)'),
        ('regression', 'Regression Model (Linear Regression)'),
        ('knn', 'K-Nearest Neighbors Classifier'),
    ]

    data_file = forms.FileField(
        label="Upload Data File"
    )
    target_column = forms.CharField(
        required=False,
        help_text="Exact name of the target column in your data. Not required for preview."
    )
    model_type = forms.ChoiceField(
        choices=MODEL_CHOICES,
        required=False,
        help_text="Select a model to train. Not required for preview."
    )
