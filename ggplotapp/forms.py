from django import forms

class NameForm(forms.Form):
    gene_name = forms.CharField(label='Gene Name', max_length=100)