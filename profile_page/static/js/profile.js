function changeTab(tabName) {
    // Get all tab content
    const tabs = document.querySelectorAll('.tab-content');
    const tabButtons = document.querySelectorAll('.tab');

    // Hide all tab contents
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all tab buttons
    tabButtons.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show the selected tab and set it as active
    document.getElementById(tabName).classList.add('active');
    document.querySelector(`.tab[onclick="changeTab('${tabName}')"]`).classList.add('active');
}


document.addEventListener('DOMContentLoaded', function () {
   
    const burgerMenu = document.getElementById("burger-menu"); // Update ID to match HTML
    const dropdownMenu = document.getElementById("dropdownMenu");

  
    // Toggle dropdown menu visibility when clicking the burger menu
    burgerMenu.addEventListener("click", () => {
        dropdownMenu.classList.toggle("active");
    });
    
});
