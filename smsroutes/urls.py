from django.urls import path
from .views import   *

urlpatterns = [
    # path("view-smsroutes/", GetRoutesView.as_view()),
    path("view-assignedroutes/<int:id>", GetAssignedRoutesView.as_view()),
    path("smsroute/", CreateRouteView.as_view()),
    path("assign-smsroute/", AssignRouteView.as_view()),
    path("remove-assigned-smsroute/", RemoveAssignedRouteView.as_view()),


    # path("view-smscs/", GetRoutesView.as_view()),
    # path("view-assigned-smsc/<int:id>", GetAssignedRoutesView.as_view()),
    # path("create-smsc/", CreateRouteView.as_view()),
    # path("assign-smsc/", AssignRouteView.as_view()),
    # path("remove-assigned-smsc/", RemoveAssignedRouteView.as_view()),

]