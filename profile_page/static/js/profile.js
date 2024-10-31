function changeTab(tab) {

    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });

   
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active'); 
    });

   
    if (tab === 'profile') {
        document.getElementById('profile').classList.add('active'); 
        tabs[0].classList.add('active');
    } else if (tab === 'account-info') {
        document.getElementById('account-info').classList.add('active');
        tabs[1].classList.add('active'); 
    }
}
