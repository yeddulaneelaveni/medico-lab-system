from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# =========================
# PATIENT
# =========================
class Patient(models.Model):
    patient_id = models.CharField(max_length=10, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient.objects.order_by('-id').first()
            next_id = last_patient.id + 1 if last_patient else 1
            self.patient_id = f"PAT{next_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"


# =========================
# TEST CATEGORY
# =========================
class TestCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# =========================
# LAB TEST
# =========================
class LabTest(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# =========================
# TEST PARAMETER
# =========================
class TestParameter(models.Model):
    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name='parameters'
    )
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    normal_range = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.lab_test.name})"


# =========================
# AUTO CREATE DEFAULT PARAMETERS
# =========================
@receiver(post_save, sender=LabTest)
def create_default_parameters(sender, instance, created, **kwargs):
    if created and instance.name == "Lipid Profile":
        TestParameter.objects.bulk_create([
            TestParameter(lab_test=instance, name="Total Cholesterol", unit="mg/dL", normal_range="< 200"),
            TestParameter(lab_test=instance, name="LDL Cholesterol", unit="mg/dL", normal_range="< 100"),
            TestParameter(lab_test=instance, name="HDL Cholesterol", unit="mg/dL", normal_range="> 40"),
            TestParameter(lab_test=instance, name="Triglycerides", unit="mg/dL", normal_range="< 150"),
            TestParameter(lab_test=instance, name="Blood Pressure", unit="mmHg", normal_range="120/80"),
            TestParameter(lab_test=instance, name="Blood Glucose", unit="mg/dL", normal_range="< 100"),
        ])


# =========================
# REPORT
# =========================
class Report(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        default='Pending'
    )

    doctor_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.patient.full_name}"


# =========================
# TEST RESULT (ONE ROW PER PARAMETER)
# =========================
class TestResult(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name='test_results'
    )
    parameter = models.ForeignKey(TestParameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.parameter.name} - {self.report.patient.full_name}"


# =========================
# AUTO CREATE TEST RESULTS WHEN REPORT IS CREATED
# =========================
@receiver(post_save, sender=Report)
def create_test_results(sender, instance, created, **kwargs):
    if created:
        parameters = instance.lab_test.parameters.all()
        for param in parameters:
            TestResult.objects.create(
                report=instance,
                parameter=param,
                value=""
            )


# =========================
# EMPLOYEE (UNCHANGED)
# =========================
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


# =========================
# EMPLOYEE ATTENDANCE
# =========================
class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('On Leave', 'On Leave')]
    )

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date}"


# =========================
# ACTIVITY LOG
# =========================
class ActivityLog(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="activity_logs"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.message}"


# =========================
# NOTIFICATION PREFERENCE
# =========================
class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_alerts = models.BooleanField(default=False)
    test_results_ready = models.BooleanField(default=True)
    system_updates = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
