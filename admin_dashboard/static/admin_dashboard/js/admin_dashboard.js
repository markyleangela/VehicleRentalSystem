function filterBookings(status) {
    const tabs = document.querySelectorAll(".tabs .tab");
    const rows = document.querySelectorAll(".bookings-table tbody tr");

    // Reset active tab
    tabs.forEach(tab => tab.classList.remove("active"));

    // Set active class for the clicked tab
    const activeTab = document.querySelector(`.tabs .tab[onclick="filterBookings('${status}')"]`);
    if (activeTab) {
        activeTab.classList.add("active");
    }

    // Reset visibility for all rows
    rows.forEach(row => {
        row.style.display = 'table-row'; // Show all rows by default
    });

    // Now filter based on status
    rows.forEach(row => {
        if (status === 'all') {
            row.style.display = 'table-row'; // Show all rows for "All"
        } else if (status === 'in-progress' && !row.classList.contains('in-progress')) {
            row.style.display = 'none'; // Hide rows that don't match "in-progress"
        } else if (status === 'completed' && !row.classList.contains('completed')) {
            row.style.display = 'none'; // Hide rows that don't match "completed"
        } else if (status === 'overdue' && !(row.classList.contains('overdue') || row.classList.contains('overdue_pending') || row.classList.contains('overdue_returned'))) {
            row.style.display = 'none'; // Hide rows that don't match "overdue"
        } else if (status === 'cancelled' && !row.classList.contains('cancelled')) {
            row.style.display = 'none'; // Hide rows that don't match "cancelled"
        }
    });
}
