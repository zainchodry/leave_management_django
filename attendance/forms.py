from django import forms
from . models import Attendance

class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = (
            "student",
            "date",
            "status",
            "remarks",
        )

        widgets = {
            "student": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter remarks",
                }
            ),
        }

class AttendanceUpdateForm(
    forms.ModelForm
):

    class Meta:

        model = Attendance

        fields = (

            "status",

            "remarks"
        )

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter remarks",
                }
            ),
        }
