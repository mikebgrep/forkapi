from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ScheduleView

app_name = "schedule"

router_schedule = SimpleRouter()
router_schedule.register(r"", ScheduleView)

urlpatterns = [
    path("", include(router_schedule.urls)),
]
