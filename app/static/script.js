document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");
    if (!calendarEl || typeof FullCalendar === 'undefined') return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridDay",
        themeSystem: "bootstrap5",
        slotMinTime: "09:00:00",
        slotMaxTime: "18:00:00",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
        },
        events: "/admin/api/bookings",
        eventDidMount: function(info) {
            const status = info.event.extendedProps.status;
            if (status === "Attended") {
                info.el.style.textDecoration = "line-through";
                info.el.style.opacity = 0.6;
            } else if (status === "No Show") {
                info.el.style.backgroundColor = "red";
            }
        },
        eventClick: function(info) {
            if (confirm("Edit this booking?")) {
                window.location.href = `/admin/booking/edit/${info.event.id}`;
            }
        }
    });

    calendar.render();
});
