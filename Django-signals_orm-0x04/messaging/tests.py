from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingTestCase(TestCase):
    def setuUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

    def test_notification_creation(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.read)


class MessageEditTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Initial content"
        )

    def test_message_edit_logs_history(self):
        # Update message content
        self.message.content = "Edited content"
        self.message.save()

        # Check if history is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Initial content")
        self.assertTrue(self.message.edited)