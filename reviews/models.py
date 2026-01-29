from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils import timezone

class Application(models.Model):
    name = models.CharField(max_length=150)
    link = models.URLField(max_length=255)
    description = models.TextField()
    category =  models.TextField()
    image = models.ImageField(upload_to="app_images/", blank=True, null=True)
    is_fraud = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class AppReview(models.Model):
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    )

    REVIEW_STATUS_CHOICES = (
        ('genuine', 'Genuine'),
        ('fake', 'Fake'),
    )

    app = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    sentiment = models.CharField(
        max_length=10,
        choices=SENTIMENT_CHOICES,
        blank=True,
        null=True
    )
    sentiment_score = models.FloatField(default=0.0)

    review_status = models.CharField(
        max_length=10,
        choices=REVIEW_STATUS_CHOICES,
        default='genuine'
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.app.name} ({self.review_status})"

    

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"
