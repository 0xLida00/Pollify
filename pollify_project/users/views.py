from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from admin_panel.utils import log_activity
from .models import User, Follow
from .forms import ProfileUpdateForm, CustomSignupForm, UserUpdateForm

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Welcome!")
            return redirect('login')
    else:
        form = CustomSignupForm()
    return render(request, 'users/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'users/login.html')


@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(followed=user_profile).count()
    following = Follow.objects.filter(follower=user_profile).count()
    is_following = Follow.objects.filter(follower=request.user, followed=user_profile).exists()

    if request.user == user_profile:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Profile updated successfully.")
                log_activity(request.user, "Updated their profile.")
                return redirect('profile', username=request.user.username)
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user)

        return render(request, 'users/profile.html', {
            'u_form': u_form,
            'p_form': p_form,
            'followers': followers,
            'following': following,
            'is_following': is_following,
            'user_profile': user_profile
        })
    else:
        # View-only profile for other users
        log_activity(request.user, f"Viewed profile of {user_profile.username}.")
        return render(request, 'users/profile_view_only.html', {
            'user_profile': user_profile,
            'followers': followers,
            'following': following,
            'is_following': is_following
        })


# Follow/Unfollow Author or User Profile
@login_required
def toggle_follow(request, user_id):
    if request.method == "POST":
        user_to_toggle = get_object_or_404(User, id=user_id)

        # Check existing follow relationship
        existing_follow = Follow.objects.filter(follower=request.user, followed=user_to_toggle).first()

        if existing_follow:
            # If already following, unfollow
            existing_follow.delete()
            return JsonResponse({"success": True, "action": "unfollow"})
        else:
            # If not following, follow
            Follow.objects.get_or_create(follower=request.user, followed=user_to_toggle)
            return JsonResponse({"success": True, "action": "follow"})

    return JsonResponse({"success": False}, status=400)


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed successfully.")
            log_activity(request.user, "Changed their password.")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/password_change.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            log_activity(request.user, "Updated their profile.")
            return redirect('profile', username=request.user.username)
    return render(request, 'users/profile_update.html', {'u_form': u_form, 'p_form': p_form})