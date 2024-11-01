function filterBookings(status) {
    const rows = document.querySelectorAll('.bookings-table tbody tr');
    rows.forEach(row => {
        row.style.display = 'table-row'; // Reset visibility
        if (status === 'in-progress' && !row.classList.contains('in-progress')) {
            row.style.display = 'none';
        } else if (status === 'completed' && !row.classList.contains('completed')) {
            row.style.display = 'none';
        }
    });

    // Update active tab styling
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`.tab[onclick="filterBookings('${status}')"]`).classList.add('active');
}


document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('vehicle-modal');
    const closeModalButton = document.getElementById('close-modal');
    const burgerMenu = document.getElementById("burger-menu");
    const dropdownMenu = document.getElementById("dropdownMenu");

    // Open modal when clicking the "View" button
    document.querySelectorAll('.view-action-button').forEach(button => {
        button.addEventListener('click', function () {
            // Get vehicle details from data attributes
            const rentalId = this.getAttribute('data-rental-id');
            const rentalVehicleId = this.getAttribute('data-vehicle-id');
            const rentalStartDate = this.getAttribute('data-rental-start-date');
            const rentalReturnDate = this.getAttribute('data-rental-return-date');
            const rentalAmount = this.getAttribute('data-rental-amount');
            const rentalPaymentDate = this.getAttribute('data-rental-payment-date');
            const rentalPaymentStatus = this.getAttribute('data-rental-payment-status');
            const rentalReturnStatus = this.getAttribute('data-rental-return-status');
            const rentalCustomer = this.getAttribute('data-rental-customer');
            const vehicleBrand = this.getAttribute('data-vehicle-brand');
            const vehicleModel = this.getAttribute('data-vehicle-model');
            const vehicle = this.getAttribute('data-rental-vehicle');
            const vehicleImg = this.getAttribute('data-vehicle-img');
            var paymentStatus = "Unpaid";
            var returnStatus = "Pending Return";

            if (rentalPaymentStatus == "True") {
                paymentStatus = "Paid";
            }

            if (rentalReturnStatus == "True") {
                returnStatus = "Returned";
            }

            document.getElementById('modal-vehicle-img').innerHTML = `
                <img src="data:image/png;base64,${vehicleImg}" alt="${vehicleModel}" style="width: 400px; height: auto;" />
            `;

            // Populate modal with vehicle details
            document.getElementById('modal-vehicle-info').innerHTML = `
                <h2>${vehicle}</h2>
                <div class='rental-vehicle-id'>
                    <h3>Rental ID: ${rentalId} | Vehicle ID: ${rentalVehicleId}</h3>
                </div>
                <div class='rental-dates'>
                    <p>Vehicle Brand:</p>
                    <p>${vehicleBrand}</p>
                    <p>Vehicle Model:</p>
                    <p>${vehicleModel}</p>
                    <p><i class="far fa-calendar"></i> Start Date:</p>
                    <p><strong>${rentalStartDate}</strong></p>
                    <p><i class="far fa-calendar"></i> Return Date:</p>
                    <p><strong>${rentalReturnDate}</strong></p>
                    <p><i class="far fa-calendar"></i> Payment Date:</p>
                    <p><strong>${rentalPaymentDate}</strong></p>
                </div>
                <div class='rental-date'>
                    <p>Payment Status: <strong>${paymentStatus}</strong></p>
                    <p>Return Status: <strong>${returnStatus}</strong></p>
                    <p><i class="far fa-user"></i> <strong>${rentalCustomer}</strong></p>
                    <p>Total Amount: <strong>${rentalAmount}</strong></p>
                </div>
            `;

            modal.style.display = 'block'; // Show the modal
        });
    });

    // Close the modal when clicking the close button
    closeModalButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Close the modal when clicking outside of the modal content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Toggle dropdown menu visibility
    burgerMenu.addEventListener("click", () => {
        dropdownMenu.classList.toggle("active");
    });
});
