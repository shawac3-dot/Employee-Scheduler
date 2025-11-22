// Filter employee table
document.getElementById('filter').addEventListener('input', function(e){
    let val = e.target.value.toLowerCase();
    document.querySelectorAll('#rows tr').forEach(tr=>{
        tr.style.display = [...tr.querySelectorAll('td')].some(td=>td.textContent.toLowerCase().includes(val)) ? '' : 'none';
    });
});

// Edit modal populate fields
var editModal = document.getElementById('editModal');
editModal.addEventListener('show.bs.modal', function(event){
    var button = event.relatedTarget;
    document.getElementById('edit-id').value = button.dataset.id;
    document.getElementById('edit-employee_id').value = button.dataset.employee_id;
    document.getElementById('edit-name').value = button.dataset.name;
    document.getElementById('edit-phone').value = button.dataset.phone;
    document.getElementById('edit-hourly_rate').value = button.dataset.hourly_rate;
});

// FullCalendar setup
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var scheduleModal = new bootstrap.Modal(document.getElementById('scheduleModal'));
    var scheduleForm = document.getElementById('scheduleForm');
    var scheduleDateInput = document.getElementById('schedule-date');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        editable: true,
        events: '/api/schedules',  // fetch events from backend
        select: function(info) {
            scheduleDateInput.value = info.startStr; // set selected date
            scheduleModal.show();
        }
    });
    calendar.render();

    // Handle modal form submit
    scheduleForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let employee_id = document.getElementById('employee-select').value;
        let start_time = document.getElementById('start-time').value;
        let end_time = document.getElementById('end-time').value;
        let date = scheduleDateInput.value;

        if(employee_id && start_time && end_time){
            fetch('/api/schedules', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ employee_id, date, start_time, end_time })
            }).then(res=>{
                if(res.ok){
                    scheduleModal.hide();
                    calendar.refetchEvents();
                    scheduleForm.reset();
                }
            });
        }
    });
});
