from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    The serializer class for user model. It will check the uniqueness of a user
    as well as store it in database
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    username = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    """A method that will validate the data send for user and will add the user"""

    def create(self, validated_data):
        user_obj = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            username=validated_data["username"],
            last_name=validated_data["last_name"],
        )
        user_obj.set_password(validated_data["password"])
        user_obj.save()
        return user_obj
