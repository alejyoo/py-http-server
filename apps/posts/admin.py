from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('id', 'author', 'created_at', 'updated_at')
  list_filter = ('created_at', 'author')
  readonly_fields = ('created_at', 'updated_at')
  list_per_page = 10
  ordering = ("-created_at",)

  fields = ("author", "content", "created_at", "updated_at")
