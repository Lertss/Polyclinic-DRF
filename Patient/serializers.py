from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from .models import Patient


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'gender',
                  'birth_date',
                  'password',
                  ]



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'region',
            'neighborhood',
            'city',
            'street',
            'house',
            'apartment',
            'allergy',
            'blood_type',
            'medical_insurance_number',
        ]

    def create(self, validated_data):
        """
        Custom behavior for creating a Patient instance.
        """
        return Patient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom behavior for updating a Patient instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
