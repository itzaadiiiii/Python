from rest_framework import viewsets

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """Provides list, retrieve, create, update, and delete operations for employees."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
