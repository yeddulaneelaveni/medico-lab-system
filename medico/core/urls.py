from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view
from .views import (
    PatientViewSet,
    TestCategoryViewSet,
    LabTestViewSet,
    ReportViewSet,
    TestResultViewSet,
    EmployeeViewSet,
    EmployeeAttendanceViewSet,
    ActivityLogViewSet,
    NotificationPreferenceViewSet,
)

router = DefaultRouter()
router.register('patients', PatientViewSet)
router.register('test-categories', TestCategoryViewSet)
router.register('lab-tests', LabTestViewSet)
router.register('reports', ReportViewSet)
router.register('test-results', TestResultViewSet)
router.register('employees', EmployeeViewSet)
router.register('attendance', EmployeeAttendanceViewSet)
router.register('activity-logs', ActivityLogViewSet)
router.register('notification-preferences', NotificationPreferenceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view),

]
