from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Employee


class EmployeeApiTests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            full_name="Ada Lovelace",
            email="ada@example.com",
            department="Engineering",
            position="Developer",
            salary="95000.00",
            hired_date=date(2024, 1, 15),
        )

    def test_create_employee(self):
        payload = {
            "full_name": "Grace Hopper",
            "email": "grace@example.com",
            "department": "Engineering",
            "position": "Admiral",
            "salary": "120000.00",
            "hired_date": "2024-02-01",
            "is_active": True,
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_list_update_and_delete_employee(self):
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.patch(
            f"/api/employees/{self.employee.pk}/",
            {"position": "Senior Developer"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], "Senior Developer")

        response = self.client.delete(f"/api/employees/{self.employee.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())
