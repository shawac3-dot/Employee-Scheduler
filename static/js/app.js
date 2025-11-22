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
