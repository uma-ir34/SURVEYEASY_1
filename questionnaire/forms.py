from django import forms
from .models import Participant
from .models import Survey


        
class ChoiceForm(forms.Form):
    text = forms.CharField(max_length=255, label='Choice Text')


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'location', 'age', 'gender', 'contact_info']

