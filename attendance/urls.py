from django.urls import path

from . import views


urlpatterns = [

    path(
        "mark/",
        views.mark_attendance,
        name="mark_attendance"
    ),

    path(
        "update/<int:pk>/",
        views.update_attendance,
        name="update_attendance"
    ),

    path(
        "my/",
        views.my_attendance,
        name="my_attendance"
    ),

    path(
        "percentage/",
        views.attendance_percentage,
        name="attendance_percentage"
    ),

    path(
        "all/",
        views.all_attendance,
        name="all_attendance"
    ),

    path(
        "statistics/",
        views.attendance_statistics,
        name="attendance_statistics"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_attendance,
        name="delete_attendance"
    ),
]