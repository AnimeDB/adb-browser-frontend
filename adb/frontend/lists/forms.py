from django import forms
from adb.frontend.lists.models import List


class ListForm(forms.ModelForm):
    name = forms.CharField(error_messages={
        'required': 'Inserisci un nome per la nuova lista da creare'
    })
    
    class Meta:
        model = List
        fields = ('name',)

