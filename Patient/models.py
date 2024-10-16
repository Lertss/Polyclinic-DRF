import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

import secured_fields
from django.utils import timezone
from django.contrib.auth.hashers import make_password

OPTIONS_GENDER = (
    ('Male', 'Male'),
    ('Other', 'Other'),
    ('Woman', 'Woman'),
)

OPTIONS_BLOOD = (
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-')
)


# add activation via phone confirmation
class CustomUser(AbstractUser):
    """Model of the main user"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = secured_fields.EncryptedCharField(max_length=50, searchable=True)
    last_name = secured_fields.EncryptedCharField(max_length=50, searchable=True)
    phone_number = secured_fields.EncryptedCharField(max_length=10, unique=True, searchable=True)
    email = secured_fields.EncryptedCharField(max_length=255, unique=True)
    gender = secured_fields.EncryptedCharField(max_length=20, choices=OPTIONS_GENDER, blank=False, null=False)
    birth_date = secured_fields.EncryptedDateField()
    created_at = secured_fields.EncryptedDateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Check if the password is set and not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Patient(models.Model):
    """
       Model of a patient
       Only after creating the CustomUser model and confirming the number can you create a patient profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, editable=False)
    region = secured_fields.EncryptedCharField(max_length=50)
    neighborhood = secured_fields.EncryptedCharField(max_length=50)
    city = secured_fields.EncryptedCharField(max_length=50)
    street = secured_fields.EncryptedCharField(max_length=50, null=True)
    house = secured_fields.EncryptedCharField(max_length=50, null=True)
    apartment = secured_fields.EncryptedCharField(max_length=50, null=True)
    allergy = secured_fields.EncryptedTextField(max_length=50)
    blood_type = secured_fields.EncryptedCharField(max_length=50, choices=OPTIONS_GENDER, blank=False, null=False)
    medical_insurance_number = secured_fields.EncryptedCharField(max_length=20,
                                                                 blank=True,
                                                                 null=True,
                                                                 searchable=True,
                                                                 unique=True)




class Record(models.Model):
    """Patient records"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = secured_fields.EncryptedTextField(max_length=50)
    doctor_autohor = models.ForeignKey('Doctor.Doctor', on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_at = secured_fields.EncryptedDateTimeField(default=timezone.now)
    updated_at = secured_fields.EncryptedDateTimeField(default=timezone.now, editable=False)
    file_analysis = secured_fields.EncryptedFileField(upload_to='record/', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     """Check whether the doctor and patient are the same user"""
    #     if self.doctor.user == self.patient.user:
    #         raise ValueError("A doctor cannot create a record for himself/herself.")
    #     super().save(*args, **kwargs)
