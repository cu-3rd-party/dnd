from django.db import models


class Player(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    telegram_id = models.BigIntegerField()
    telegram_username = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    pfp = models.ImageField(upload_to="pfps/", null=True)
    bio = models.TextField(blank=True)
    admin = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = "players"

    def __str__(self):
        return f"{self.telegram_username or self.telegram_id}"
