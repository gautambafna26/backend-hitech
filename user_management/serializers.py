from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for reading User objects (non-sensitive fields).
    """
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role")
        read_only_fields = ("id",)


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating users. Accepts a plain-text password
    and uses set_password() so the password is stored hashed.
    Validates that email is unique.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer used for registering a new user.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Authenticate a user and return the user object as `validated_data`.
    The view expects `serializer.validated_data` to be the user instance.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Return the user object itself; the view expects this value.
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating the authenticated user's profile."""
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "role")
        read_only_fields = ("id", "username",)

    def update(self, instance, validated_data):
        # Prevent changing username via this serializer
        validated_data.pop('username', None)
        return super().update(instance, validated_data)


class UserPermissionsSerializer(serializers.Serializer):
    """Return a summary of a user's permission-related attributes."""
    is_superuser = serializers.BooleanField(source='is_superuser')
    is_staff = serializers.BooleanField(source='is_staff')
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        try:
            return sorted(list(obj.get_all_permissions()))
        except Exception:
            return []


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for allowing users to change their password."""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        old = attrs.get('old_password')
        new = attrs.get('new_password')
        confirm = attrs.get('confirm_password')

        if user is None:
            raise serializers.ValidationError('User is required in context for password change')

        if not user.check_password(old):
            raise serializers.ValidationError({'old_password': 'Old password is not correct'})

        if new != confirm:
            raise serializers.ValidationError({'confirm_password': "New passwords do not match"})

        return {
            'new_password': new
        }