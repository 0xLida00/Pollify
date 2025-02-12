document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap 4 dropdowns
    $('.dropdown-toggle').dropdown();

    // Auto-close dropdown when clicking outside
    document.addEventListener('click', function (event) {
        const openDropdown = document.querySelector('.dropdown.show');

        if (openDropdown) {
            const dropdownToggle = openDropdown.querySelector('.dropdown-toggle');

            if (!openDropdown.contains(event.target)) {
                $(dropdownToggle).dropdown('hide');  // Use jQuery to close the dropdown if clicked outside
            }
        }
    });

    // Prevent default dropdown toggle if it doesn't open correctly
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function (event) {
            event.preventDefault();  // Avoid default behavior that may interfere with dropdown
            $(this).dropdown('toggle');  // Manually toggle the dropdown
        });
    });

    // Handle "Mark as Read" action via AJAX
    document.querySelectorAll('.mark-as-read').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const notificationId = this.dataset.notificationId;

            fetch(`/notifications/mark-as-read/${notificationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const listItem = this.closest('.list-group-item');
                    if (listItem) {
                        listItem.classList.remove('bg-light');
                        this.remove();
                    }
                    updateNotificationBadgeCount();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Handle "Mark All as Read" action via AJAX
    document.getElementById('mark-all-as-read')?.addEventListener('click', function (event) {
        event.preventDefault();

        fetch('/notifications/mark-all-as-read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelectorAll('.mark-as-read').forEach(button => button.remove());
                document.querySelectorAll('.list-group-item.bg-light').forEach(item => item.classList.remove('bg-light'));
                updateNotificationBadgeCount(0);
            }
        })
        .catch(error => console.error('Error marking all notifications as read:', error));
    });

    // Function to update the notification badge count
    function updateNotificationBadgeCount(newCount = null) {
        const badge = document.querySelector('#notificationDropdown .notification-badge');
        if (badge) {
            let count = newCount !== null ? newCount : (parseInt(badge.textContent, 10) || 0) - 1;
            badge.textContent = count > 0 ? count : '';
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
            const [key, value] = cookies[i].split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return '';
    }
});