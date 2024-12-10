function loadModal() {
    const modal = document.getElementById('confirmationModal');
    const submitBtn = document.getElementById('btn-submit');
    const form = document.getElementById('contact-form');
   

    
    // Submit the form to delete the vehicle if the confirm button is clicked
    submitBtn.addEventListener('click', function() {
        form.submit(); // Submit the form to delete the vehicle
        modal.style.display = "none"; // Hide the modal after confirming
    });

    // Close the modal if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
}

// Attach event listeners to all delete buttons
document.querySelectorAll('.btn-submit').forEach(function(submitBtn) {
    submitBtn.addEventListener('click', function(event) {
        loadModal();  // Load and show the modal for the clicked vehicle
    });
});