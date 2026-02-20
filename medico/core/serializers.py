from rest_framework import serializers
from django.contrib.auth.models import User

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
# USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active'
        ]


# =========================
# PATIENT SERIALIZER
# =========================
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id', 'created_at']


# =========================
# TEST CATEGORY SERIALIZER
# =========================
class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = '__all__'


# =========================
# LAB TEST SERIALIZER
# =========================
class LabTestSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    class Meta:
        model = LabTest
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'price'
        ]


# =========================
# TEST RESULT SERIALIZER
# (This gives parameter name + value box)
# =========================
class TestResultSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(
        source='parameter.name',
        read_only=True
    )
    unit = serializers.CharField(
        source='parameter.unit',
        read_only=True
    )
    normal_range = serializers.CharField(
        source='parameter.normal_range',
        read_only=True
    )

    class Meta:
        model = TestResult
        fields = [
            'id',
            'parameter_name',
            'unit',
            'normal_range',
            'value'
        ]


# =========================
# REPORT SERIALIZER
# (Final report structure like your Figma)
# =========================
class ReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source='patient.full_name',
        read_only=True
    )
    patient_id = serializers.CharField(
        source='patient.patient_id',
        read_only=True
    )
    test_name = serializers.CharField(
        source='lab_test.name',
        read_only=True
    )

    test_results = TestResultSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Report
        fields = [
            'id',
            'patient',
            'patient_name',
            'patient_id',
            'lab_test',
            'test_name',
            'status',
            'doctor_remarks',
            'created_at',
            'test_results'
        ]


# =========================
# EMPLOYEE SERIALIZER
# (UNCHANGED)
# =========================
class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'employee_id',
            'department',
            'role',
            'mobile_number',
            'is_active'
        ]


# =========================
# EMPLOYEE ATTENDANCE
# =========================
class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.user.get_full_name',
        read_only=True
    )

    class Meta:
        model = EmployeeAttendance
        fields = '__all__'


# =========================
# ACTIVITY LOG SERIALIZER
# =========================
class ActivityLogSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.user.get_full_name',
        read_only=True
    )

    class Meta:
        model = ActivityLog
        fields = '__all__'


# =========================
# NOTIFICATION PREFERENCE
# =========================
class NotificationPreferenceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NotificationPreference
        fields = '__all__'
