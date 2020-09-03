"""Serialize user data."""

from rest_framework import serializers

from .models import Region, STT, User


class STTSerializer(serializers.ModelSerializer):
    """STT serializer."""

    code = serializers.SerializerMethodField()

    class Meta:
        """Metadata."""

        model = STT
        fields = ["id", "type", "code", "name"]

    def get_code(self, obj):
        """Return the state code."""
        if obj.type == STT.STTType.TRIBE:
            return obj.state.code
        return obj.code


class RegionSerializer(serializers.ModelSerializer):
    """Region serializer."""

    stts = STTSerializer(many=True)

    class Meta:
        """Metadata."""

        model = Region
        fields = ["id", "stts"]


class UserSerializer(serializers.ModelSerializer):
    """Define meta user serializer class."""

    class Meta:
        """Define meta user serializer attributes."""

        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


class CreateUserSerializer(serializers.ModelSerializer):
    """Defined class to create the user serializer."""

    def create(self, validated_data):
        """Serialize the user object."""
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        """Define meta user serializer attributes."""

        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}


class SetUserProfileSerializer(serializers.ModelSerializer):
    """Serializer used for setting a user's profile."""

    class Meta:
        """Metadata."""

        model = User
        fields = ["first_name", "last_name", "requested_role", "stt"]

    def validate_requested_role(self, value):
        """Validate that the requested role can be set.

        This can only be set if there is no `role` or `requested_role` already set.
        """
        user = self.context["request"].user
        if user.role:
            raise serializers.ValidationError(
                "Cannot set requested role after a role is set."
            )
        if user.requested_role:
            raise serializers.ValidationError(
                "Cannot modify requested role after it is set."
            )
        return value

    def validate_stt(self, value):
        """Validate that the STT cannot be changed once set."""
        if self.context["request"].user.stt:
            raise serializers.ValidationError("Cannot modify STT after it is set.")
        return value
