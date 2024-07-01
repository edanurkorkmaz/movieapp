from django.db import models
from django.db import models
from django.contrib.auth.models import User

class FavoriteMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Untitled Movie")

    def __str__(self):
        return self.title