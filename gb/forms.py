from django import forms

class ResumeForm(forms.Form):
    pdf = forms.FileField()
    photo = forms.ImageField()
