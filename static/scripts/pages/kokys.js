const signupForm = document.querySelector('#signup-form');
const signinForm = document.querySelector('#signin-form');
const signupFormChanger = document.querySelector('#signupFormChanger');
const signinFormChanger = document.querySelector('#signinFormChanger');

const loader = document.querySelector('.loader__overlay');

const signupFullName = document.querySelector('#fullname')
const signupEmail = document.querySelector('#email')
const signupPassword = document.querySelector('#password')
const signupConfirmPassword = document.querySelector('#confirmpassword')

const signinEmail = document.querySelector('#signinemail')
const signinPassword = document.querySelector('#signinpassword')

function changeModeToIn() {
    signupForm.classList.remove('signing-form_active');
    signinForm.classList.add('signing-form_active');
}

function changeModeToUp() {
    signinForm.classList.remove('signing-form_active');
    signupForm.classList.add('signing-form_active');
}

function confirmedPasswordCheck(firstPassword, secondPassword) {
    return firstPassword === secondPassword;
}

function isValid(typeOfSign) {
    valid = true;
    if (typeOfSign === 'signup-form'){

        const inputs = signupForm.querySelectorAll('.signing-form__input');
        
        if (inputs[1].value.includes('@')){
            inputs.forEach((input) => {
                if (input.value === '' || (input.value).length < 3) {
                    valid = false;
                    console.log(valid);
                }
            })
        }
        else {
            valid = false;
        }
        console.log(valid);
        return valid
    } 
}

function formSubmitHandler(e){
    e.preventDefault();
    signUser(e.target.id);
}



function signUser(typeOfSign) {
    renderLoader(true);
    if (typeOfSign === 'signup-form' && isValid(typeOfSign)){
        
        const username = signupFullName.value;
        const email = signupEmail.value;
        const firstPass = signupPassword.value;
        const secondPass = signupConfirmPassword.value;

        if (confirmedPasswordCheck(firstPass, secondPass)) {

            fetch('/sign_up_check/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    userFullName: username,
                    userEmail: email,
                    userPassword: firstPass
                })
            })

            .then((res) => {
                if (res.ok) {
                    console.log('You was registered!')
                    renderLoader(false);
                    signupForm.reset();
                    changeModeToIn();
                }
                else{
                    console.log('э че то не то')
                }
            })

        }

    }

    else if (typeOfSign === 'signin-form'){

        console.log('signin was done!');

    }
    
    
}

signupForm.addEventListener('submit', formSubmitHandler)
signinForm.addEventListener('submit', formSubmitHandler)

