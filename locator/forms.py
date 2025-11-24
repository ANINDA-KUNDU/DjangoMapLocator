from django import forms
from locator.models import Search

class SearchForm(forms.ModelForm):
    address = forms.CharField(label = '')
    class Meta:
        model = Search
        fields = '__all__'