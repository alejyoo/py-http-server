from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [("A", "Administrator"), ("M", "Moderator"), ("U", "User")]

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("N", "Prefer not to say"),
    ]

    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text="Bio (500 char. maximum)",
    )

    date_of_birth = models.DateField(help_text="Obligatory.")

    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )

    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOICES,
        default="U",
    )

    profile_pic = models.ImageField(
        upload_to="profile-pics/",
        null=True,
        blank=True,
        verbose_name="Profile picture",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def get_age(self):
        from datetime import date

        today = date.today()
        age = today.year - self.date_of_birth.year

        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month
            and today.day < self.date_of_birth.day
        ):
            age -= 1

        return age

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def is_admin(self):
        return self.role == "A"

    def is_moderator(self):
        return self.role == "M"

    def has_profile_pic(self):
        return bool(self.profile_pic)

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.date_of_birth and self.date_of_birth >= timezone.now().date():
            raise ValidationError(
                {"date_of_birth": "The date of birth is after this date."}
            )

        if self.date_of_birth and self.get_age() < 18:
            raise ValidationError(
                {"date_of_birth": "You must've at least 18 to register."}
            )
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __repr__(self):
        return (
            f"User(name='{self.get_full_name()}', "
            f"email='{self.email}', "
            f"active={self.is_active})"
        )
