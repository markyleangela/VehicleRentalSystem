function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('imagePreview').src = e.target.result;
    };
    reader.readAsDataURL(event.target.files[0]);
}

document.addEventListener('DOMContentLoaded', function () {
   
    const burgerMenu = document.getElementById("burger-menu"); // Update ID to match HTML
    const dropdownMenu = document.getElementById("dropdownMenu");

  
    // Toggle dropdown menu visibility when clicking the burger menu
    burgerMenu.addEventListener("click", () => {
        dropdownMenu.classList.toggle("active");
    });
    
});