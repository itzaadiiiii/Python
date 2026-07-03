from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
        ('Engineering', 'Engineering'),
        ('Legal', 'Legal'),
        ('Customer Support', 'Customer Support'),
        ('Research', 'Research & Development'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Yes', 'Married'),
        ('No', 'Single'),
    ]

    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    age = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    birthdate = models.DateField()
    marital_status = models.CharField(
        max_length=3,
        choices=MARITAL_STATUS_CHOICES,
        default='No'
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return self.full_name

    @property
    def calculated_age(self):
        """Calculate age from birthdate"""
        today = timezone.now().date()
        born = self.birthdate
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
