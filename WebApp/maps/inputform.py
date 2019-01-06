from django import forms
from maps.models import DataTable

#This class contains form fields like start, end, mode
class InputForm(forms.ModelForm):

    MODE_CHOICES = [ ('DRIVING', 'DRIVING'), ('WALKING', 'WALKING')]

    Start = forms.CharField(label='Start Location', max_length=100)
    End = forms.CharField(label='Destination', max_length=100)
    Mode = forms.CharField(label='Mode', widget=forms.Select(choices=MODE_CHOICES))

    #meta class links the model with the form
    class Meta:
        model = DataTable
        fields = ('Start', 'End', 'Mode',)
