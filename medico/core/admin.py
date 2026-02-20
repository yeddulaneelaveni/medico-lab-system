from django.contrib import admin
from .models import (
    Patient,
    TestCategory,
    LabTest,
    TestParameter,
    Report,
    TestResult,
    Employee,
    EmployeeAttendance,
    ActivityLog,
    NotificationPreference
)

# =========================
# INLINE: Test Parameters (inside LabTest)
# =========================
class TestParameterInline(admin.TabularInline):
    model = TestParameter
    extra = 0


# =========================
# INLINE: Test Results (inside Report)
# =========================
class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0                    # 🔥 No empty rows
    can_delete = False           # 🔥 Prevent deleting auto-created rows
    readonly_fields = ('parameter',)  # 🔥 Show parameter name but don’t edit


# =========================
# PATIENT ADMIN
# =========================
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'full_name', 'age', 'gender', 'mobile_number')
    search_fields = ('patient_id', 'full_name', 'mobile_number')
    list_filter = ('gender',)


# =========================
# TEST CATEGORY ADMIN
# =========================
@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# =========================
# LAB TEST ADMIN
# =========================
@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [TestParameterInline]   # 🔥 Shows parameters inside LabTest


# =========================
# REPORT ADMIN
# =========================
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'lab_test', 'status', 'created_at')
    list_filter = ('status', 'lab_test')
    search_fields = ('patient__full_name',)
    inlines = [TestResultInline]      # 🔥 Shows parameters automatically


# =========================
# EMPLOYEE ADMIN
# =========================
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'role', 'is_active')
    list_filter = ('department', 'role', 'is_active')
    search_fields = ('employee_id', 'user__username')


# =========================
# EMPLOYEE ATTENDANCE ADMIN
# =========================
@admin.register(EmployeeAttendance)
class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'date')


# =========================
# ACTIVITY LOG ADMIN
# =========================
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'message', 'created_at')


# =========================
# NOTIFICATION PREFERENCE ADMIN
# =========================
@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email_notifications',
        'sms_alerts',
        'test_results_ready',
        'system_updates'
    )
