document.addEventListener('DOMContentLoaded', function () {
    console.log("🔽 Notifications JS Loaded");

    // ✅ Ensure Bootstrap Dropdown is properly initialized
    $('.dropdown-toggle').each(function () {
        let $dropdown = $(this);
        if (!$dropdown.data('bs.dropdown')) {
            $dropdown.dropdown(); // Initialize if not already done
        }
    });

    // ✅ Handle dropdown toggle manually if needed
    document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function (event) {
            console.log("🔽 Dropdown Clicked");
            event.stopPropagation(); // Prevent immediate closing
        });
    });

    // ✅ Close dropdown when clicking outside
    document.addEventListener('click', function (event) {
        const openDropdown = document.querySelector('.dropdown.show');
        if (openDropdown && !openDropdown.contains(event.target)) {
            console.log("🔽 Closing dropdown due to outside click");
            $(openDropdown.querySelector('.dropdown-toggle')).dropdown('hide');
        }
    });

    // ✅ Handle "Mark as Read" action via AJAX
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('mark-as-read')) {
            event.preventDefault();
            const notificationId = event.target.dataset.notificationId;

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
                    console.log(`✅ Notification ${notificationId} marked as read`);
                    event.target.closest('.list-group-item').classList.remove('bg-light');
                    event.target.remove(); // Remove "Mark as Read" button
                    updateNotificationBadgeCount(); // Update badge count
                }
            })
            .catch(error => console.error('❌ Error marking notification as read:', error));
        }
    });

    // ✅ Handle "Mark All as Read" action via AJAX
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
                console.log("✅ All notifications marked as read");
                document.querySelectorAll('.mark-as-read').forEach(button => button.remove());
                document.querySelectorAll('.list-group-item.bg-light').forEach(item => item.classList.remove('bg-light'));
                updateNotificationBadgeCount(0); // Reset the count
            }
        })
        .catch(error => console.error('❌ Error marking all notifications as read:', error));
    });

    // ✅ Function to update the notification badge count dynamically
    function updateNotificationBadgeCount(newCount = null) {
        const badge = document.querySelector('#notificationDropdown .notification-badge');
        if (badge) {
            let count = newCount !== null ? newCount : (parseInt(badge.textContent, 10) || 0) - 1;
            count = count < 0 ? 0 : count; // Ensure count never goes negative
            badge.textContent = count > 0 ? count : '';
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }

    // ✅ Helper function to get CSRF token
    function getCookie(name) {
        const cookies = document.cookie.split('; ');
        for (let i = 0; i < cookies.length; i++) {
            const [key, value] = cookies[i].split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return '';
    }
});