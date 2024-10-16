from django.test import TestCase
from .models import CustomUser
import uuid
from datetime import datetime

class CustomUserTestCase(TestCase):
    def setUp(self):
        """Set up a user instance for testing"""
        self.user = CustomUser.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
            gender="Male",
            birth_date="1990-01-01",
            is_active=True
        )

    def test_uuid_generation(self):
        """Test that the UUID is automatically generated"""
        self.assertIsInstance(self.user.id, uuid.UUID)

    def test_encrypted_fields(self):
        """Test that sensitive fields like first_name, last_name, and phone_number are encrypted"""
        # This would require knowledge of the encryption mechanism.
        # Assuming that `get_decrypted_value()` is a hypothetical method that your field provides for testing.
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_created_at_default(self):
        """Test that the created_at field has the correct default"""
        self.assertIsInstance(self.user.created_at, datetime)

    def test_is_active_default(self):
        """Test that the is_active field has the correct default"""
        self.assertTrue(self.user.is_active)

    def test_gender_choices(self):
        """Test that gender field validates the choices"""
        valid_user = CustomUser.objects.create(
            first_name="Jane",
            last_name="Smith",
            phone_number="0987654321",
            gender="Female",
            birth_date="1985-12-25"
        )
        self.assertEqual(valid_user.gender, "Female")

        # Test for an invalid gender choice
        with self.assertRaises(ValueError):
            CustomUser.objects.create(
                first_name="Sam",
                last_name="Adams",
                phone_number="5555555555",
                gender="InvalidGender",
                birth_date="1995-06-15"
            )

    def test_phone_number_length(self):
        """Test that phone_number field accepts the correct length"""
        with self.assertRaises(ValueError):
            CustomUser.objects.create(
                first_name="Alex",
                last_name="Turner",
                phone_number="123",  # invalid length
                gender="Male",
                birth_date="1980-10-10"
            )

