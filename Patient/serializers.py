from djoser.serializers import UserCreatePasswordRetypeSerializer


class CustomUserCreatePasswordRetypeSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = ['id',
                  'username',
                  'email',
                  'first_name',
                  'last_name',
                  'password',]