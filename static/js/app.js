// Client-side filter for employees
const filter = document.getElementById('filter');
const rows = document.getElementById('rows');

filter?.addEventListener('input', () => {
  const q = filter.value.toLowerCase();
  for (const tr of rows.querySelectorAll('tr')) {
    const employee_id  = tr.querySelector('.employee_id')?.textContent.toLowerCase() || '';
    const name         = tr.querySelector('.name')?.textContent.toLowerCase() || '';
    const phone        = tr.querySelector('.phone')?.textContent.toLowerCase() || '';
    const hourly_rate  = tr.querySelector('.hourly_rate')?.textContent.toLowerCase() || '';
    const total_hours  = tr.querySelector('.total_hours')?.textContent.toLowerCase() || '';

    tr.style.display = (
      employee_id.includes(q) ||
      name.includes(q) ||
      phone.includes(q) ||
      hourly_rate.includes(q) ||
      total_hours.includes(q)
    ) ? '' : 'none';
  }
});

// Edit modal populate
const editModal = document.getElementById('editModal');
editModal?.addEventListener('show.bs.modal', (ev) => {
  const btn = ev.relatedTarget;
  document.getElementById('edit-id').value           = btn.getAttribute('data-id');
  document.getElementById('edit-employee_id').value  = btn.getAttribute('data-employee_id');
  document.getElementById('edit-name').value         = btn.getAttribute('data-name');
  document.getElementById('edit-phone').value        = btn.getAttribute('data-phone');
  document.getElementById('edit-hourly_rate').value  = btn.getAttribute('data-hourly_rate');
});
