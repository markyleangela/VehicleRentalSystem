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

    // Open modal when clicking the "View" button
    document.querySelectorAll('.view-action-button').forEach(button => {
        button.addEventListener('click', function () {
            // Get vehicle details from data attributes
            const rentalId = this.getAttribute('data-rental-id');
            const rentalVehicleId = this.getAttribute('data-vehicle-id');
            const rentalStartDate = this.getAttribute('data-rental-start-date');
            const rentalReturnDate = this.getAttribute('data-rental-return-date');
            const rentalAmount = this.getAttribute('data-rental-amount');
            const rentalPaymentDate = this.getAttribute('data-rental-payment-date')
            const rentalPaymentStatus= this.getAttribute('data-rental-payment-status')
            const rentalCustomer= this.getAttribute('data-rental-customer')
            const vehicleBrand = this.getAttribute('data-vehicle-brand');
            const vehicleModel = this.getAttribute('data-vehicle-model');



            // Populate modal with vehicle details
            document.getElementById('modal-vehicle-info').innerHTML = `
                <div class='rental-vehicle-id'>
                    <h3>Rental ID: ${rentalId} | Vehicle ID: ${rentalVehicleId}</h3>
                </div>

                <div class='vehicle-details'>
       
                    <p> Vehicle Brand: ${vehicleBrand}</p>
                    <p> Vehicle Model ${vehicleModel}</p>
                </div>

                <div class='rental-dates'>
       
                    <p><i class="fas fa-calendar-alt"></i> Start Date: ${rentalStartDate}</p>
                    <p><i class="fas fa-calendar-alt"></i> Return Date: ${rentalReturnDate}</p>
                    <p><i class="fas fa-calendar-alt"></i> Payment Date: ${rentalPaymentDate}</p>
                </div>

                <div class='rental-date'>
       
                    <p> Payment Status: ${rentalPaymentStatus}</p>
                    <p>User: ${rentalCustomer}</p>
                    <p> Total Amount: ${rentalAmount}</p>
                    
                </div>

                



               
          

              
            `;

            // document.getElementById('modal-vehicle-img').innerHTML = `
            //     <img src="${vehicleImg}" alt="${vehicleModel}" style="width: 100%; max-width: 550px;"/>
            // `;

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
});

