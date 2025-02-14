from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages as flash_messages
from .models import Message
from .forms import ComposeMessageForm

# Use custom or default user model
User = get_user_model()

@login_required
def inbox(request):
    """View for the user's inbox with filtering and pagination."""
    filter_param = request.GET.get('filter', 'all')

    # Filter messages by the recipients field
    mailbox_messages = Message.objects.filter(recipients=request.user).order_by('-sent_at')

    # Apply filter for unread messages if requested
    if filter_param == 'unread':
        mailbox_messages = mailbox_messages.filter(is_read=False)

    paginator = Paginator(mailbox_messages, 10)
    page_number = request.GET.get('page', 1)
    messages_page = paginator.get_page(page_number)

    return render(request, 'messaging/inbox.html', {
        'mailbox_messages': messages_page,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': messages_page,
        'active_tab': 'inbox',
        'filter_param': filter_param,
    })


@login_required
def outbox(request):
    """View for the user's sent messages."""
    mailbox_messages = request.user.sent_messages.order_by('-sent_at')
    paginator = Paginator(mailbox_messages, 10)  # Show 10 messages per page
    page_number = request.GET.get('page', 1)
    messages_page = paginator.get_page(page_number)

    return render(request, 'messaging/outbox.html', {
        'mailbox_messages': messages_page,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': messages_page,
        'active_tab': 'outbox',
    })


@login_required
def compose_message(request):
    """View to compose a new message with support for multiple recipients."""
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST, sender=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            form.save_m2m()  # Save recipients
            flash_messages.success(request, 'Your message has been sent successfully.')
            return redirect('messaging:inbox')  # Ensure redirection happens
    else:
        form = ComposeMessageForm(sender=request.user)

    return render(request, 'messaging/compose_message.html', {
        'form': form,
        'active_tab': 'compose',
    })


@login_required
def read_message(request, message_id):
    """View a specific message received by the user."""
    message = get_object_or_404(Message, id=message_id, recipients=request.user)

    # Mark the message as read if it hasn't been read yet
    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'messaging/read_message.html', {
        'message': message,
        'active_tab': 'inbox',
    })


@login_required
def message_detail(request, message_id):
    """View a specific message sent by the user."""
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    
    return render(request, 'messaging/message_detail.html', {
        'message': message,
        'active_tab': 'outbox',
    })