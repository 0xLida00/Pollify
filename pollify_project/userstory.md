# Pollify – A Social Polling Platform

## Project Overview
Pollify is an interactive social polling platform that allows users to create, share, and participate in polls. Users can vote, comment, follow others, receive notifications, and engage in private messaging. The system will have a clear user hierarchy, including regular users and administrators.

---

## User Roles
1. Anonymous User (Unregistered)
2. Registered User (Authenticated)
3. Administrator (Superuser)

---

## User Stories by Role

### 1. Anonymous User (Unregistered)
*As an unregistered user, I want to:*
- View public polls to explore available content.
- Sign up for an account to participate in polls.
- Log in to access personalized content and discussions.
- Browse poll categories without restrictions.
- View trending polls to see popular content.

---

### 2. Registered User (Authenticated)

*As a registered user, I want to:*
#### Poll Management
- Create new polls to gather opinions.
- Set expiration dates on polls to control voting duration.
- Add multiple choices to my poll.
- View and edit my own polls.
- Archive/delete my polls if no longer relevant.

#### Voting System
- Vote on available polls.
- View poll results after voting.
- Change my vote within the poll duration.

#### Commenting System
- Comment on polls to engage in discussions.
- Edit or delete my own comments.
- View comments from other users.

#### Following System
- Follow other users to stay updated.
- Receive notifications for followed user activities.
- View my followers and followings list.

#### Notifications
- Receive notifications for comments on my poll.
- Get notified when my poll reaches a milestone.
- Dismiss notifications after viewing them.

#### Messaging System
- Send private messages to other users.
- Receive and reply to messages.
- View inbox and outbox.
- Mark messages as read/unread.

#### Profile Management
- Update my bio and profile picture.
- Change my email and password securely.
- View my poll history and participation.

#### User Engagement
- Like or share polls.
- Report inappropriate content.

---

### 3. Administrator (Superuser)

*As an administrator, I want to:*
#### User Management
- View and manage all users.
- Assign/revoke admin privileges.
- Reset user passwords.

#### Poll Moderation
- View and delete flagged polls.
- Edit polls violating guidelines.
- Moderate comments.

#### Analytics and Reports
- View poll engagement analytics.
- Generate reports on poll popularity.
- Send announcements to users.

#### System Management
- Configure poll visibility and security policies.
- Manage the database of polls and users.
- Oversee profile picture storage.

---

## Summary of Functionalities to Implement

### 1. User Authentication & Profile
- Register/Login/Logout
- Password reset
- Profile management (bio, avatar)
- User roles (User/Admin)

### 2. Poll Creation and Management
- Create/Edit/Delete polls
- Poll expiration handling
- Add poll choices
- Poll visibility (private/public)

### 3. Voting System
- Cast vote (one-time restriction)
- Change vote (optional within duration)
- View poll results

### 4. Comments System
- Add/Edit/Delete comments
- View comments with timestamps

### 5. User Following System
- Follow/unfollow users
- View followers/following lists
- Receive updates from followed users

### 6. Notifications
- Real-time or periodic notifications
- Notify users on new poll creation and comments
- Mark notifications as read

### 7. Private Messaging
- Send/receive messages
- View inbox and outbox
- Mark messages as read/unread
- Delete messages

### 8. Admin Dashboard
- View/manage users, polls, and comments
- Analytics (poll engagement, top users)
- Reports and content moderation

### 9. Search and Filtering
- Search polls by keyword
- Filter polls by category, date, or popularity

### 10. Reporting & Moderation
- Report abusive polls or comments
- Admin review and decision-making
- Automated moderation tools (e.g., content flagging)

---

## Django Apps to Create in the Project

To modularize the project, following Django apps will be created:

1. **`users`** (Handles authentication, profiles, and follow system)
   - Models: `User`, `Follow`
   - Views: Signup, Login, Profile Management
   - Templates: Registration, Profile Page

2. **`polls`** (Manages polls, choices, and votes)
   - Models: `Poll`, `Choice`, `Vote`
   - Views: Poll creation, voting, results
   - Templates: Poll creation form, results display

3. **`comments`** (Handles comments on polls)
   - Models: `Comment`
   - Views: Add/Edit/Delete comment
   - Templates: Comment sections on polls

4. **`notifications`** (Manages user notifications)
   - Models: `Notification`
   - Views: Notifications list, mark as read
   - Templates: Notification dropdown/list

5. **`messaging`** (Handles private user messaging)
   - Models: `Message`
   - Views: Inbox, Outbox, Compose message
   - Templates: Messaging interface

6. **`admin_panel`** (For administrative management and analytics)
   - Models: None (Uses Django admin)
   - Views: Analytics dashboard, user moderation
   - Templates: Dashboard UI

7. **`frontend`** (For UI presentation using HTML, CSS, and JS)
   - Static files: CSS, JS, Images
   - Templates: Base templates and homepage


## Pollify Entity-Relationship Diagram
