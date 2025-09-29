from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import date
from .models import User
from django.utils import timezone


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "bio",
            "date_of_birth",
            "gender",
            "profile_pic",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords does not match."}
            )

        if attrs["date_of_birth"] >= timezone.now().date():
            raise serializers.ValidationError(
                {"date_of_birth": "Date of birth cannot be in the future."}
            )

        today = date.today()
        age = today.year - attrs["date_of_birth"].year
        if today.month < attrs["date_of_birth"].month or (
            today.month == attrs["date_of_birth"].month
            and today.day < attrs["date_of_birth"].day
        ):
            age -= 1

        if age < 18:
            raise serializers.ValidationError(
                {"date_of_birth": "Debes tener al menos 18 años para registrarte."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        if "first_name" in validated_data:
            validated_data["first_name"] = validated_data["first_name"].strip().title()

        if "last_name" in validated_data:
            validated_data["last_name"] = validated_data["last_name"].strip().title()

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    has_profile_pic = serializers.SerializerMethodField()
    is_admin = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "bio",
            "date_of_birth",
            "age",
            "gender",
            "role",
            "profile_pic",
            "has_profile_pic",
            "is_admin",
            "is_moderator",
            "is_active",
            "created_at",
            "updated_at",
            "last_activity",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "role",
            "is_active",
            "created_at",
            "updated_at",
            "last_activity",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_age(self, obj):
        return obj.get_age() if obj.date_of_birth else None

    def get_has_profile_pic(self, obj):
        return obj.has_profile_pic()

    def get_is_admin(self, obj):
        return obj.is_admin()

    def get_is_moderator(self, obj):
        return obj.is_moderator()
