from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count
from .models import Poll, Choice, Vote
from .forms import PollForm
from users.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Home view
def home(request):
    return render(request, "home.html")


# List View for Polls with Pagination and Filtering
class PollListView(ListView):
    model = Poll
    template_name = "polls/poll_list.html"
    context_object_name = "polls"
    paginate_by = 5  # Show 5 polls per page

    def get_queryset(self):
        queryset = Poll.objects.annotate(total_votes=Count("votes"))
        filter_by = self.request.GET.get("filter_by", "").strip()
        value = self.request.GET.get("value", "").strip()
        sort_by = self.request.GET.get("sort_by", "").strip()

        # Ensure filtering works properly
        if filter_by and value:
            if filter_by == "category":
                queryset = queryset.filter(category__icontains=value)  # Case-insensitive filter
            elif filter_by == "author":
                queryset = queryset.filter(author__username__icontains=value)
            elif filter_by == "expires":
                try:
                    queryset = queryset.filter(expires_at__date=value)
                except ValueError:
                    pass  # Ignore invalid date input

        # Sorting Logic
        if sort_by == "newest":
            queryset = queryset.order_by("-created_at")
        elif sort_by == "oldest":
            queryset = queryset.order_by("created_at")
        elif sort_by == "most_voted":
            queryset = queryset.order_by("-total_votes")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_paginated"] = self.paginate_by and self.get_queryset().count() > self.paginate_by
        context["filter_by"] = self.request.GET.get("filter_by", "")
        context["value"] = self.request.GET.get("value", "")
        context["sort_by"] = self.request.GET.get("sort_by", "")
        return context


# Poll Creation View
class PollCreateView(LoginRequiredMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/poll_form.html"
    success_url = reverse_lazy("poll_list")

    def form_valid(self, form):
        poll = form.save(commit=False)
        poll.author = self.request.user
        poll.save()

        choices_text = form.cleaned_data["choices"]
        choices = [choice.strip() for choice in choices_text.split("\n") if choice.strip()]
        if len(choices) < 2:
            raise ValidationError("You must provide at least two choices.")

        for choice_text in choices:
            Choice.objects.create(poll=poll, choice_text=choice_text)

        messages.success(self.request, "Poll created successfully!")
        return redirect(self.success_url)


# Poll Detail View
class PollDetailView(DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        total_votes = poll.votes.count()
        choices_with_percentages = []

        for choice in poll.choices.all():
            percentage = (choice.votes_count / total_votes * 100) if total_votes > 0 else 0
            choices_with_percentages.append({
                "choice_text": choice.choice_text,
                "votes_count": choice.votes_count,
                "percentage": round(percentage, 2),
            })

        context["choices_with_percentages"] = choices_with_percentages
        context["total_votes"] = total_votes
        context["can_vote"] = self.request.user.is_authenticated
        if self.request.user.is_authenticated and self.request.user != poll.author:
            context["is_following"] = poll.author.followers.filter(id=self.request.user.id).exists()
        return context


# Poll Detail View
class PollEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Poll
    fields = ['description', 'expires_at']  # Allow editing only these fields
    template_name = "polls/poll_edit.html"
    success_url = reverse_lazy("poll_list")

    def test_func(self):
        poll = self.get_object()
        return self.request.user == poll.author  # Only author can edit

    def form_valid(self, form):
        messages.success(self.request, "Poll updated successfully!")
        return super().form_valid(form)
    

# Handle Voting
@login_required
def vote_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    
    if request.method == "POST":
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(Choice, id=choice_id, poll=poll)

        # Check if user already voted
        if Vote.objects.filter(poll=poll, voter=request.user).exists():
            messages.error(request, "You have already voted on this poll.")
            return redirect("poll_detail", pk=poll.pk)

        # Save vote
        Vote.objects.create(poll=poll, choice=choice, voter=request.user)
        choice.votes_count += 1
        choice.save()

        # Send WebSocket update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"poll_{poll.id}",
            {"type": "update_poll", "poll_id": poll.id}
        )

        messages.success(request, "Your vote has been recorded successfully!")
        return redirect("poll_detail", pk=poll.pk)

    return redirect("poll_detail", pk=poll.pk)


# Follow/Unfollow Author
@login_required
def toggle_follow(request, user_id):
    """Toggle follow/unfollow functionality."""
    author = get_object_or_404(User, id=user_id)
    if request.user in author.followers.all():
        author.followers.remove(request.user)
        return JsonResponse({"success": True, "action": "unfollow"})
    else:
        author.followers.add(request.user)
        return JsonResponse({"success": True, "action": "follow"})


# Poll Deletion View
class PollDeleteView(LoginRequiredMixin, DeleteView):
    model = Poll
    template_name = "polls/poll_confirm_delete.html"
    success_url = reverse_lazy("poll_list")

    def dispatch(self, request, *args, **kwargs):
        poll = self.get_object()
        if poll.author != request.user:
            messages.error(request, "You do not have permission to delete this poll.")
            return redirect("poll_list")
        return super().dispatch(request, *args, **kwargs)