from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    username = None  # Remove username field, use email instead

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Removes email from REQUIRED_FIELDS

    def __str__(self):
        return self.email


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, through='ConversationParticipant', related_name='conversations')

    def __str__(self):
        return f"Conversation {self.id}"


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"{self.user} in {self.conversation}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message {self.id} by {self.sender}"
