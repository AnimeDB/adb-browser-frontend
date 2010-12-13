from django import forms

from adb.frontend.collection.models import Movie
from adb.frontend.lists.models import List


class MovieListsForm(forms.Form):
    lists = forms.ModelMultipleChoiceField(queryset=None, required=False)
    
    def __init__(self, queryset, *args, **kwargs):
        super(MovieListsForm, self).__init__(*args, **kwargs)
        self.fields["lists"].queryset = queryset
    