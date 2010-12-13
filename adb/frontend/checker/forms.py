import re

from django import forms


class AnimeDBTopicID(forms.IntegerField):
    def to_python(self, value):
        try:
            return int(re.search(r'\d+', value).group(0))
        except (ValueError, AttributeError):
            raise forms.ValidationError("Inserisci un indirizzo corretto.")

class CheckForm(forms.Form):
    id = AnimeDBTopicID(error_messages={
        'required': 'Inserisci l\'indirizzo del topic della release.'
    })