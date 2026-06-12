from django.urls import path
from . import views

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("<int:pk>/", views.notification_detail, name="notification_detail"),
    path("read/<int:pk>/", views.mark_as_read, name="mark_as_read"),
    path("read-all/", views.mark_all_read, name="mark_all_read"),
    path("delete/<int:pk>/", views.delete_notification, name="delete_notification"),
    path("announcements/", views.announcements, name="announcements"),
    path("announcements/create/", views.create_announcement, name="create_announcement"),
    path("announcements/delete/<int:pk>/", views.delete_announcement, name="delete_announcement"),
]