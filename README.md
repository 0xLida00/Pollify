# Pollify 🗳️

Pollify is an interactive polling platform that allows users to create, vote, and discuss polls. It also includes a messaging system, notifications, and an admin panel for managing user activity. The platform is built with Django and Bootstrap 4 for a seamless and user-friendly experience.
---

## I/ 🚀 Features

### ✅ Poll System
- Create, edit, and delete polls
- Vote on polls and view real-time results
- Comment on polls and engage in discussions
- Search and filter polls by category

### 📩 Messaging System
- Send and receive private messages
- Support for multiple recipients
- Mark messages as read
- Filter and paginate inbox/outbox messages

### 🔔 Notifications
- Receive alerts for new messages and poll interactions
- View unread and read notifications
- Mark notifications as read

### 👥 User Management
- User authentication (signup, login, logout)
- Profile pages with avatars and bio
- Follow/unfollow users
- Edit user profile details

### 📊 Admin Panel
- Admin dashboard for monitoring user activity
- View and filter activity logs
- Manage polls, comments, and users

### 🔎 Search & Filtering
- Search polls by keywords
- Filter polls by categories
- Filter inbox messages by read/unread status
- Admin log filtering by user actions
---

## II/ 🛠️ Tech Stack

### Backend
- [Django](https://www.djangoproject.com/) (Python Web Framework)
- SQLite (Default Database, can be replaced with PostgreSQL/MySQL)

### Frontend
- [Bootstrap 4](https://getbootstrap.com/) (CSS Framework)
- HTML, CSS, and JavaScript

### Other Dependencies
- Django Authentication (for user management)
- Django Messages Framework (for notifications)
- Django Pagination (for messages and polls)
---

## III/ 🏗️ Installation

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/pollify.git
cd pollify

### 2️⃣ Create & Activate Virtual Environment
python3 -m venv pollify_env
source pollify_env/bin/activate  # On Windows use: pollify_env\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Apply Migrations
python manage.py migrate

### 5️⃣ Create a Superuser (For Admin Panel)
python manage.py createsuperuser

### 6️⃣ Run the Development Server
python manage.py runserver

### Visit http://127.0.0.1:8000/ in your browser to access the platform.
---

## IV/ 🧪 Running Tests
Pollify includes unit tests to ensure functionality is working correctly.

### Run all tests:
python manage.py test

### Run specific app tests:
python manage.py test messaging
python manage.py test polls
---

## V/ 📌 To-Do / Future Enhancements
	•	Add poll analytics & insights
	•	Implement poll sharing feature
	•	Improve UI/UX for mobile responsiveness
	•	Introduce more notification types
	•	Enable real-time updates using WebSockets
---

### VI/ 🤝 Contribution
Contributions are welcome! Follow these steps to contribute:
	1.	Fork the repo.
	2.	Create a new branch: git checkout -b feature-new-feature
	3.	Commit changes: git commit -m "Added new feature"
	4.	Push to branch: git push origin feature-new-feature
	5.	Open a Pull Request
---

## VII/ 📁 Project Structure
```
pollify_project/
│── admin_panel/        # Admin dashboard module
│── comments/           # Poll comment system
│── frontend/           # frontend files/codes
│── messaging/          # Private messaging system
│── notifications/      # User notifications
│── pollify_project/    # Django project settings
│── polls/              # Polls and voting system
│── users/              # User authentication and profiles
│── static/             # CSS, JS, images
│── manage.py           # Django project management script
│── requirements.txt    # Dependencies
│── README.md           # Project documentation