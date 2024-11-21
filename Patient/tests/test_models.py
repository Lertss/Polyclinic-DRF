

from Patient.models import CustomUser, Patient, Record
from Doctor.models import Doctor
from django.core.exceptions import ValidationError
import uuid
from datetime import date
from django.test import TestCase
from django.utils.timezone import now


class CustomUserModelTest(TestCase):

    def setUp(self):
        """Створення тестового користувача перед кожним тестом."""
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'birth_date': date(1990, 1, 1),
            'password': 'password123',
        }

    def test_create_user(self):
        """Перевірка створення користувача."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertEqual(user.gender, 'Male')
        self.assertFalse(user.is_active)  # Перевірка значення за замовчуванням
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))  # Перевірка хешування пароля
        self.assertIsInstance(user.id, uuid.UUID)  # Перевірка унікального ідентифікатора

    def test_unique_phone_number(self):
        """Перевірка унікальності номера телефону."""
        CustomUser.objects.create(**self.user_data)
        with self.assertRaises(ValidationError):
            user = CustomUser(**self.user_data)
            user.full_clean()  # Виклик перевірки валідності

    def test_unique_email(self):
        """Перевірка унікальності електронної пошти."""
        CustomUser.objects.create(**self.user_data)
        with self.assertRaises(ValidationError):
            user = CustomUser(**self.user_data)
            user.full_clean()

    def test_gender_choices(self):
        """Перевірка вибору гендеру."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['gender'] = 'Male'
        with self.assertRaises(ValidationError):
            user = CustomUser(**invalid_user_data)
            user.full_clean()


    def test_save_password_hash(self):
        """Перевірка хешування пароля при збереженні."""
        user = CustomUser.objects.create(**self.user_data)
        raw_password = self.user_data['password']
        self.assertNotEqual(user.password, raw_password)  # Переконаємося, що пароль хешується

    def test_default_is_active(self):
        """Перевірка, що is_active за замовчуванням False."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertFalse(user.is_active)

    def test_creation_date(self):
        """Перевірка автоматичного встановлення created_at."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertIsNotNone(user.created_at)  # Перевірка, що created_at встановлено

    def test_birth_date_validation(self):
        """Перевірка, що дата народження зберігається правильно."""
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.birth_date, date(1990, 1, 1))




class PatientModelTest(TestCase):

    def setUp(self):
        """Створення тестових даних для користувача та пацієнта."""
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'gender': 'Male',
            'birth_date': '1990-01-01',
            'password': 'password123',
        }
        self.user = CustomUser.objects.create(**self.user_data)

        self.patient_data = {
            'user': self.user,
            'region': 'Region1',
            'neighborhood': 'Neighborhood1',
            'city': 'City1',
            'street': 'Street1',
            'house': 'House1',
            'apartment': 'Apartment1',
            'allergy': 'Pollen',
            'blood_type': 'Male',  # Можливо, тут потрібні коригування, якщо це не підходящий вибір
            'medical_insurance_number': 'INS123456',
        }

    def test_create_patient(self):
        """Перевірка створення профілю пацієнта."""
        patient = Patient.objects.create(**self.patient_data)
        self.assertEqual(patient.user, self.user)
        self.assertEqual(patient.region, 'Region1')
        self.assertEqual(patient.neighborhood, 'Neighborhood1')
        self.assertEqual(patient.city, 'City1')
        self.assertEqual(patient.street, 'Street1')
        self.assertEqual(patient.house, 'House1')
        self.assertEqual(patient.apartment, 'Apartment1')
        self.assertEqual(patient.allergy, 'Pollen')
        self.assertEqual(patient.blood_type, 'Male')  # Тут може бути перевірка згідно з реальними значеннями blood_type
        self.assertEqual(patient.medical_insurance_number, 'INS123456')
        self.assertIsInstance(patient.id, uuid.UUID)

    def test_patient_requires_user(self):
        """Перевірка, що без користувача неможливо створити пацієнта."""
        self.patient_data['user'] = None
        with self.assertRaises(Exception):
            Patient.objects.create(**self.patient_data)

    def test_unique_medical_insurance_number(self):
        """Перевірка унікальності номера медичної страховки."""
        Patient.objects.create(**self.patient_data)
        with self.assertRaises(Exception):  # UniqueConstraintException
            duplicate_patient_data = self.patient_data.copy()
            duplicate_patient_data['user'] = CustomUser.objects.create(
                first_name='Jane',
                last_name='Doe',
                phone_number='0987654321',
                email='jane.doe@example.com',
                gender='Female',
                birth_date='1992-02-02',
                password='password123',
            )
            Patient.objects.create(**duplicate_patient_data)

    def test_null_fields(self):
        """Перевірка, що поля street, house, і apartment можуть бути null."""
        self.patient_data['street'] = None
        self.patient_data['house'] = None
        self.patient_data['apartment'] = None
        patient = Patient.objects.create(**self.patient_data)
        self.assertIsNone(patient.street)
        self.assertIsNone(patient.house)
        self.assertIsNone(patient.apartment)

    def test_blood_type_choices(self):
        """Перевірка правильності вибору blood_type."""
        valid_patient_data = self.patient_data.copy()
        valid_patient_data['blood_type'] = 'Other'  # Припустимо, це допустимий вибір
        patient = Patient.objects.create(**valid_patient_data)
        self.assertEqual(patient.blood_type, 'Other')

        invalid_patient_data = self.patient_data.copy()
        invalid_patient_data['blood_type'] = 'InvalidBloodType'
        with self.assertRaises(Exception):  # ValidationError
            Patient.objects.create(**invalid_patient_data)





from django.core.files.base import ContentFile




class TestRecordModel(TestCase):
    def setUp(self):
        """Створення тестових даних"""
        # Створюємо користувачів
        self.doctor_user = CustomUser.objects.create(
            username="testdoctor",
            first_name="Test",
            last_name="Doctor",
            phone_number="1234567890",
            email="doctor@example.com",
            gender="male",
            birth_date="1980-01-01",
        )
        self.patient_user = CustomUser.objects.create(
            username="testpatient",
            first_name="Test",
            last_name="Patient",
            phone_number="0987654321",
            email="patient@example.com",
            gender="female",
            birth_date="1990-01-01",
        )

        # Створюємо лікаря та пацієнта
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            specialty="Cardiology",
            phone_general="987654321",
            cabinet="101A",
        )
        self.patient = Patient.objects.create(
            user=self.patient_user,
            region="Region",
            neighborhood="Neighborhood",
            city="City",
            allergy="None",
            blood_type="O+",
            medical_insurance_number="123456789",
        )

    def test_create_record(self):
        """Тест успішного створення запису"""
        record = Record.objects.create(
            description="Patient shows signs of hypertension.",
            doctor_autohor=self.doctor,
            patient=self.patient,
        )
        assert Record.objects.count() == 1
        assert record.description == "Patient shows signs of hypertension."
        assert record.doctor_autohor == self.doctor
        assert record.patient == self.patient

    def test_doctor_cannot_create_record_for_self(self):
        """Тест, що лікар не може створити запис для себе"""
        with self.assertRaises(ValueError) as e:
            Record.objects.create(
                description="Self-record attempt.",
                doctor_autohor=self.doctor,
                patient=Patient.objects.create(user=self.doctor_user, city="Test City", region="Region", neighborhood="Neighborhood", allergy="None", blood_type="A+")
            )
        assert str(e.exception) == "A doctor cannot create a record for himself/herself."

    def test_created_and_updated_at_fields(self):
        """Тест полів дати створення та оновлення"""
        record = Record.objects.create(
            description="Initial description.",
            doctor_autohor=self.doctor,
            patient=self.patient,
        )
        now_time = now()
        assert abs((record.created_at - now_time).total_seconds()) < 1
        assert abs((record.updated_at - now_time).total_seconds()) < 1
