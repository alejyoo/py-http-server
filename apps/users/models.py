from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [("A", "Administrator"), ("M", "Moderator"), ("U", "User")]
    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text="Bio (500 char. maximum)",
    )

    date_of_birth = models.DateField(help_text="Obligatory.")

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

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone

        if self.date_of_birth >= timezone.now().date():
            raise ValidationError(
                {"date_of_birth": "The date of birth is after this date."}
            )

        self.first_name.lower().capitalize()
        self.last_name.lower().capitalize()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def __repr__(self):
        return f"""{self.first_name} {self.last_name}
        {self.role} ({self.email})
        IS ACTIVE: {self.is_active}"""
