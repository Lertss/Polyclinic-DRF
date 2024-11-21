from Patient.models import CustomUser
from Doctor.models import Doctor, OpeningHours
from django.test import TestCase
from datetime import time

class DoctorModelTest(TestCase):

    def setUp(self):
        """Set up test environment"""
        self.user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            gender="Male",
            birth_date="1990-01-01",
            password="testpassword123"
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialty="Cardiologist",
            phone_general="9876543210",
            cabinet="101"
        )

    def test_doctor_creation(self):
        """Test creation of a doctor"""
        self.assertEqual(self.doctor.user, self.user)
        self.assertEqual(self.doctor.specialty, "Cardiologist")
        self.assertEqual(self.doctor.phone_general, "9876543210")
        self.assertEqual(self.doctor.cabinet, "101")

    def test_doctor_user_relationship(self):
        """Test doctor is linked to a user"""
        self.assertEqual(self.doctor.user.first_name, "John")
        self.assertEqual(self.doctor.user.last_name, "Doe")

    def test_invalid_specialty(self):
        """Test specialty cannot be blank"""
        with self.assertRaises(Exception):
            Doctor.objects.create(
                user=self.user,
                specialty="",  # Invalid specialty
                phone_general="9876543210",
                cabinet="102"
            )

class TestOpeningHoursModel(TestCase):

    def setUp(self):
        """Створення тестових даних"""
        self.user = CustomUser.objects.create(
            username="testdoctor",
            first_name="Test",
            last_name="Doctor",
            phone_number="1234567890",
            email="doctor@example.com",
            gender="male",
            birth_date="1980-01-01",
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialty="Cardiology",
            phone_general="987654321",
            cabinet="101A",
        )
        self.opening_hour = OpeningHours.objects.create(
            weekday=1,
            open_hour=time(9, 0),
            close_hour=time(17, 0),
            doctor=self.doctor,
        )

    def test_create_opening_hours(self):
        """Тест успішного створення запису"""
        assert OpeningHours.objects.count() == 1
        opening_hour = OpeningHours.objects.first()
        assert opening_hour.weekday == 1
        assert opening_hour.open_hour == time(9, 0)
        assert opening_hour.close_hour == time(17, 0)

    def test_unique_together_constraint(self):
        """Тест унікальності записів"""
        with self.assertRaises(Exception):
            OpeningHours.objects.create(
                weekday=1,
                open_hour=time(9, 0),
                close_hour=time(17, 0),
                doctor=self.doctor,
            )

    def test_ordering(self):
        """Тест сортування записів"""
        OpeningHours.objects.create(
            weekday=2,
            open_hour=time(10, 0),
            close_hour=time(15, 0),
            doctor=self.doctor,
        )
        hours = OpeningHours.objects.all()
        assert list(hours) == sorted(hours, key=lambda h: (h.weekday, h.open_hour))

    def test_unicode_representation(self):
        """Тест методу __str__"""
        hour = OpeningHours.objects.first()
        assert str(hour.open_hour) == "09:00:00"
        assert str(hour.close_hour) == "17:00:00"
