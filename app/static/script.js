document.addEventListener("DOMContentLoaded", function() {
    var calendarEl = document.getElementById("calendar");
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridDay",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
        },
        themeSystem: "bootstrap5",
        height: "auto",
        slotMinTime: "09:00:00",
        slotMaxTime: "18:00:00",
        events: "/admin/api/bookings",

        eventDidMount: function(info) {
            if (info.event.extendedProps.status === "Attended") {
                info.el.style.textDecoration = "line-through";  // Strikethrough
                info.el.style.opacity = "0.6";  // Dim the color
            } else if (info.event.extendedProps.status === "No Show") {
                info.el.style.backgroundColor = "red";  // Highlight no-shows in red
            }
        },

        eventClick: function(info) {
            if (confirm("Edit this booking?")) {
                window.location.href = "/admin/booking/edit/" + info.event.id;
            }
        }
    });
    calendar.render();
});

// Handle status update buttons
document.querySelectorAll(".update-status").forEach(button => {
    button.addEventListener("click", function() {
        var bookingId = this.getAttribute("data-id");
        var newStatus = this.getAttribute("data-status");

        fetch(`/admin/api/update-status/${bookingId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                location.reload();  // Refresh page after update
            } else {
                alert("Error updating status");
            }
        });
    });
});
