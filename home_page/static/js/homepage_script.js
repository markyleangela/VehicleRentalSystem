document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('vehicle-modal');
    const closeModalButton = document.getElementById('close-modal');
    const burgerMenu = document.getElementById("burger-menu"); // Update ID to match HTML
    const dropdownMenu = document.getElementById("dropdownMenu");

    // Open modal when clicking the "View" button
    document.querySelectorAll('.view-button').forEach(button => {
        button.addEventListener('click', function () {
            // Get vehicle details from data attributes
            const vehicleBrand = this.getAttribute('data-vehicle-brand');
            const vehicleModel = this.getAttribute('data-vehicle-model');
            const vehicleType = this.getAttribute('data-vehicle-type');
            const vehiclePrice = this.getAttribute('data-vehicle-price');
            const vehicleImg = this.getAttribute('data-vehicle-image');

            // Populate modal with vehicle details
            document.getElementById('modal-vehicle-info').innerHTML = `
                <img src="${vehicleImg}" alt="${vehicleModel}" style="width: 100%; max-width: 300px;"/>
                <h3>${vehicleBrand}</h3>
                <h3>${vehicleModel}</h3>
                <p>${vehicleType}</p>
                <p class="vehicle-price">Php ${vehiclePrice}/day</p>
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

    // Toggle dropdown menu visibility when clicking the burger menu
    burgerMenu.addEventListener("click", () => {
        // Toggle dropdown menu display
        dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });
});
