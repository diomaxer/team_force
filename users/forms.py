from django import forms
from .models import User


class CreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
