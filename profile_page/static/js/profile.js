function changeTab(tab) {
    // Hide all tab contents
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.classList.remove('active'); // Remove active class to hide content
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active'); // Remove active class from tabs
    });

    // Show the selected tab content and set the clicked tab as active
    if (tab === 'profile') {
        document.getElementById('profile').classList.add('active'); // Show Profile content
        tabs[0].classList.add('active'); // Set Profile tab as active
    } else if (tab === 'account-info') {
        document.getElementById('account-info').classList.add('active'); // Show Account Information content
        tabs[1].classList.add('active'); // Set Account Information tab as active
    }
}
