from django.core.validators import MinLengthValidator as Min
from django.db import models

from apps.users.models import User


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="Author of the post",
        verbose_name="Author",
    )
    title = models.CharField(
        max_length=100,
        help_text="Title of the post",
        verbose_name="Title",
        validators=[Min(1, "Post must be at least 1 character long.")],
    )
    content = models.TextField(
        max_length=400,
        help_text="Post (400 char. maximum)",
        validators=[Min(1, "Post must be at least 1 character long.")],
        verbose_name="Content",
    )
    image = models.ImageField(
        upload_to="post-images/",
        null=True,
        blank=True,
        verbose_name="Image",
        help_text="Optional Image",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
