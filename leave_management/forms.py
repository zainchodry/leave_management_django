from django import forms
from .models import LeaveRequest

class LeaveForm(
    forms.ModelForm
):

    class Meta:

        model = LeaveRequest

        fields = (

            "leave_type",

            "start_date",

            "end_date",

            "reason"
        )

        widgets = {

            "leave_type":
            forms.Select(
                choices=LeaveRequest.LEAVE_TYPE_CHOICES,
                attrs={
                    "class": "form-control"
                }
            ),

            "start_date":
            forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date":
            forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "reason":
            forms.Textarea(
                attrs={
                    "class": "form-control"
                }
            )
        }

class LeaveReviewForm(
    forms.ModelForm
):

    class Meta:

        model = LeaveRequest

        fields = (

            "status",

            "teacher_remark"
        )

        widgets = {
            "status":
            forms.Select(
                choices=LeaveRequest.STATUS_CHOICES,
                attrs={
                    "class": "form-control"
                }
            ),

            "teacher_remark":
            forms.Textarea(
                attrs={
                    "class": "form-control"
                }
            )
        }
