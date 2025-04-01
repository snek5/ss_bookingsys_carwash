document.addEventListener("DOMContentLoaded", function() {
    var calendarEl = document.getElementById("calendar");

    if (!calendarEl) {
        console.error("Calendar element not found!");
        return;  // Prevent error if calendar is missing
    }

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridDay",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
        },
        themeSystem: "bootstrap5", // Bootstrap styling
        height: "auto",
        events: "/admin/api/bookings", // Fetch bookings dynamically
        
        // ⏰ Limit calendar time range
        slotMinTime: "09:00:00",  // Start from 9 AM
        slotMaxTime: "18:00:00",  // End at 6 PM
        
        eventClick: function(info) {
            if (confirm("Edit this booking?")) {
                window.location.href = "/admin/booking/edit/" + info.event.id;
            }
        }
    });

    calendar.render();
});
