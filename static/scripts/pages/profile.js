const navbarBtns = document.querySelectorAll('.navbar__linktext');
navbarBtns.forEach((btn) => {
    btn.classList.remove('navbar__linktext_active');
})
document.querySelector('.navbar__avatar').classList.add('navbar__avatar_active');

const userAvatarInput = document.querySelector('.user__input');
const userdataForm = document.querySelector('.userdata');

const loader = document.querySelector('.loader__overlay');

function renderLoader(isLoading) {
    if (isLoading) {
        loader.classList.add('loader_active');
    }
    else {
        loader.classList.remove('loader_active');
    }
}

function sendData(e) {
    e.preventDefault();
    const firstname = document.querySelector('#firstname').value;
    const lastname = document.querySelector('#lastname').value;
    const middlename = document.querySelector('#middlename').value;
    const phonenumber = document.querySelector('#phonenumber').value;
    const email = document.querySelector('#email').value;
    const city = document.querySelector('#city').value;
    const homeaddress = document.querySelector('#homeaddress').value;
    renderLoader(true);
    fetch('/save_data/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            firstname: firstname,
            email: email,
            lastname: lastname,
            middlename: middlename,
            phonenumber: phonenumber,
            city: city,
            homeaddress: homeaddress
        })
    }).then((res) => {
        if (res.ok) {
            renderLoader(false);
        }
        else if (res.status !== 200){
            renderLoader(false);
        }
    })
}

userAvatarInput.addEventListener('change', () => {
    renderLoader(true);
    document.querySelector('.user__image').src = URL.createObjectURL(userAvatarInput.files[0]);
    document.querySelector('.user__image').setAttribute('style', 'opacity: .6');
    document.querySelector('#userformSubmitBtn').classList.remove('userdata__submitBtn_disactive');
    document.querySelector('.user__label').classList.add('userdata__submitBtn_disactive');
    renderLoader(false);
})

document.querySelector('#userForm').addEventListener('submit', () => {
    renderLoader(true);
})
userdataForm.addEventListener('submit', sendData)