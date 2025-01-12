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


class ThreadedConversationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        # Create root message
        self.root_message = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Root message"
        )

        # Create replies
        self.reply1 = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="First reply", parent_message=self.root_message
        )
        self.reply2 = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="Second reply", parent_message=self.root_message
        )
        self.sub_reply = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="Sub-reply", parent_message=self.reply1
        )

    def test_threaded_conversation(self):
        # Test recursive retrieval of all replies
        replies = self.root_message.get_all_replies()
        self.assertEqual(len(replies), 3)  # All replies, including sub-replies

        # Test prefetching and select_related
        with self.assertNumQueries(2):  # Ensure query optimization
            messages = Message.objects.filter(parent_message=None).select_related(
                "sender", "receiver"
            ).prefetch_related("replies__sender", "replies__receiver")
            list(messages)  # Trigger evaluation
