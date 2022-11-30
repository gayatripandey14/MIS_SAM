from django.urls import path
from .views import   *

urlpatterns = [
    path("view-campaigns/", GetCampaigns.as_view()),
    path("view-campaign-schedules/", GetScheduledCampaigns.as_view()),
    path("stop-campaign/", StopRunningCampaign.as_view()),
]