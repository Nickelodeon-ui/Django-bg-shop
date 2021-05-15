# pylint: skip-file

from django import forms

class Search_BG_form(forms.Form):
    bg_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        "class": "search_form_input", "placeholder": "Введите название игры"}))

class Submit_BG_form(forms.Form):
    customer_name = forms.CharField(required=False)
    message = forms.CharField(label="Ваше сообщение",
                              widget=forms.Textarea, required=True)
