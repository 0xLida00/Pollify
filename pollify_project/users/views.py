from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
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
        return render(request, 'users/profile_view_only.html', {
            'user_profile': user_profile,
            'followers': followers,
            'following': following,
            'is_following': is_following
        })


@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, id=user_id)
        request.user.following.add(user_to_follow)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
def unfollow_user(request, user_id):
    if request.method == "POST":
        user_to_unfollow = get_object_or_404(User, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return JsonResponse({"success": True})
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
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/password_change.html', {'form': form})