from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id)

    if request.method == "POST":
        new_content = request.POST.get("content")
        if new_content and new_content != message.content:
            message.content = new_content
            message.edited_by = request.user # Track the user who made the edit
            message.edited_at = now() # Update the edit timestamp
            message.save()
        
        return redirect("view_message", message_id=message_id)
    return render(request, "edit_messasge.html", {"message": message})


@login_required
def delete_user(request):
    '''
    Deletes the currently logged-in user's account and cleans up related data.
    '''
    user = request.user
    user.delete() # Triggers the post_delete signal
    return redirect("home") # Redirect to the homepage after deletion
