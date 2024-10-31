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
            const vehicleDesc = this.getAttribute('data-vehicle-desc');
            const vehicleTrans = this.getAttribute('data-vehicle-transmission');
            const vehicleCargo = this.getAttribute('data-vehicle-cargo');

            // Populate modal with vehicle details
            document.getElementById('modal-vehicle-info').innerHTML = `
                <div class='brand-model-price'><h3>${vehicleBrand} ${vehicleModel}</h3>
                    <p class="vehicle-price">Php ${vehiclePrice}/day</p>
                </div>
   
                <div class='vehicle-specs'> 
                    <div class='specs-1'>
                        <p><i class="fas fa-car"></i> ${vehicleType}</p>
                        <p><i class="fas fa-suitcase"></i>${vehicleCargo}</p>
                    </div>

                    <div class='specs-2'>
                        <p><i class="fas fa-cog"></i>${vehicleTrans}</p>
                        <p><i class="fas fa-road"></i> Unlimited Mileage</p>
                    </div>
                    
                    
                </div>

                
                <p> ${vehicleDesc}</p>

                <div class='book-button'>
                    <button >BOOK</button>
                </div>
                
            `;

            document.getElementById('modal-vehicle-img').innerHTML = `
                <img src="${vehicleImg}" alt="${vehicleModel}" style="width: 400px; height: auto;" />
                
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
        dropdownMenu.classList.toggle("active");
    });
    
});
