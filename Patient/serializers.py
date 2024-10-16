class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=GENDER_SELECTION, required=True)
    adult = serializers.BooleanField(required=True)
    avatar = serializers.ImageField(
        default="static/images/avatars/user/none_avatar_user.jpg", allow_null=True, required=False
    )

    def custom_signup(self, request, user):
        user.gender = self.validated_data.get("gender")
        user.avatar = self.validated_data.get("avatar")
        user.save(update_fields=["gender", "avatar"])
