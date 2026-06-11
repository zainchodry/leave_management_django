from django.urls import path

from . import views

urlpatterns = [

    path(
        "apply/",
        views.apply_leave,
        name="apply_leave"
    ),

    path(
        "my-leaves/",
        views.my_leaves,
        name="my_leaves"
    ),

    path(
        "cancel/<int:pk>/",
        views.cancel_leave,
        name="cancel_leave"
    ),

    path(
        "pending/",
        views.pending_leaves,
        name="pending_leaves"
    ),

    path(
        "review/<int:pk>/",
        views.review_leave,
        name="review_leave"
    ),

    path(
        "all/",
        views.all_leaves,
        name="all_leaves"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_leave,
        name="delete_leave"
    ),

    path(
        "statistics/",
        views.leave_statistics,
        name="leave_statistics"
    ),
]