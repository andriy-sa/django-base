from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Person(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "Persons"
        verbose_name_plural = "Persons List"
        ordering = ["-created_at"]


class Comment(models.Model):
    message = models.TextField()
    rate    = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    person = models.ForeignKey(Person,related_name='comments',on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments List"
        ordering = ["-id"]


