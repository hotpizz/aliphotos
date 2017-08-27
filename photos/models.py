from django.db import models


class Photo(models.Model):
    url = models.CharField(max_length=1024, unique=True)
    item_id = models.CharField(max_length=64)
    category_id = models.CharField(max_length=64)
    feedback_id = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField()
    height = models.IntegerField()


class Like(models.Model):
    session_key = models.CharField(max_length=64)
    photo = models.ForeignKey(Photo)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'photo')


class Flag(models.Model):
    session_key = models.CharField(max_length=64)
    photo = models.ForeignKey(Photo)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64)
