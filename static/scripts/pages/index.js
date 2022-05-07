const menuBtn = document.querySelector('.navbar__menuBtn');
const navbar = document.querySelector('.navbar');

menuBtn.addEventListener('click', navbarHandler)

function openNavbar() {
    navbar.classList.toggle('navbar_active');
}

function navbarHandler(e) {
    openNavbar();
}

let navbarBtns = document.querySelectorAll('.navbar__linktext');

navbarBtns.forEach((btn) => {
    btn.classList.remove('navbar__linktext_active');
}) 

document.querySelector('#navbarMain').classList.add('navbar__linktext_active');