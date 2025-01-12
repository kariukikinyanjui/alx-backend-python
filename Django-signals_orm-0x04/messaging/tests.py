from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory
from django.utils.timezone import now


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
        self.message.edited_by = self.user1
        self.message.edited_at = now()
        self.message.save()

        # Check if history is created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Initial content")
        self.assertTrue(self.message.edited)
        self.assertIsNotNone(self.message.edited_at)
        self.assertEqual(self.message.edited_by, self.user1)


class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Test message")
        self.notification = Notification.objects.create(user=self.user2, message=self.message)

    def test_user_deletion_cleans_up_related_data(self):
        # Verify initial counts
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

        # Delete user1 and check cleanup
        self.user1.delete()
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)
