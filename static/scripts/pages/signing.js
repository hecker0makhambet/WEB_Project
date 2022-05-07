const signupFormChanger = document.querySelector('#signupFormChanger');
const signinFormChanger = document.querySelector('#signinFormChanger');


const loader = document.querySelector('.loader__overlay');


const signinEmail = document.querySelector('#signinemail')
const signinPassword = document.querySelector('#signinpassword')

function changeModeToIn() {
    signupForm.hide();
    signupForm.reset();
    signupFormValidation.clearErrors();
    signinForm.show();
}

function changeModeToUp() {
    signinForm.hide();
    signinForm.reset();
    signinFormValidation.clearErrors();
    signupForm.show();
}

function confirmedPasswordCheck(firstPassword, secondPassword) {
    return firstPassword === secondPassword;
}

function renderLoader(isLoading) {
    if (isLoading) {
        loader.classList.add('loader_active');
    }
    else {
        loader.classList.remove('loader_active');
    }
}

class FormValidator {
    constructor(settings, formSelector) {
        this._settings = settings;
        this._formSelector = formSelector;
    }

    checkButtonState() {
        this._toggleButtonState();

        // this._inputList.forEach((inputElement) => {
        //     this._isValid(inputElement);
        // });
    }

    clearErrors() {
        this._inputList.forEach((inputElement) => {
            this._hideInputError(inputElement);
        });
    }

    enableValidation() {
        this._form = document.querySelector(this._formSelector);

        // Переберём полученную коллекцию
        this._form.addEventListener('submit', (evt) => {
            // У каждой формы отменим стандартное поведение
            evt.preventDefault();
        });

        // Для каждой формы вызовем функцию setEventListeners,
        // передав ей элемент формы
        this._setEventListeners();
    };

    _setEventListeners() {
        // Находим все поля внутри формы,
        // сделаем из них массив методом Array.from
        this._inputList = Array.from(this._form.querySelectorAll(this._settings.inputSelector));
        this._buttonElement = this._form.querySelector(this._settings.submitButtonSelector);
        // Обойдём все элементы полученной коллекции
        this._toggleButtonState();
        this._inputList.forEach((inputElement) => {
            // каждому полю добавим обработчик события input
            inputElement.addEventListener('input', () => {
                // Внутри колбэка вызовем isValid,
                // передав ей форму и проверяемый элемент
                this._isValid(inputElement);
                this._toggleButtonState();
            });
        });
    };

    _isValid(inputElement) {
        if (!inputElement.validity.valid) {
            // showInputError теперь получает параметром форму, в которой
            // находится проверяемое поле, и само это поле
            this._showInputError(inputElement, inputElement.validationMessage);
        } else {
            // hideInputError теперь получает параметром форму, в которой
            // находится проверяемое поле, и само это поле
            this._hideInputError(inputElement);
        }
    };

    _showInputError(inputElement, errorMessage) {
        // Находим элемент ошибки внутри самой функции
        const errorElement = this._form.querySelector(`#${inputElement.id}-error`);
        // Остальной код такой же
        errorElement.textContent = errorMessage;
    };

    _hideInputError(inputElement) {
        // Находим элемент ошибки
        const errorElement = this._form.querySelector(`#${inputElement.id}-error`);
        // Остальной код такой же
        inputElement.classList.remove(this._settings.inputErrorClass);
        errorElement.textContent = '';
    };

    _toggleButtonState() {
        // Если есть хотя бы один невалидный инпут
        if (this._hasInvalidInput()) {
            // сделай кнопку неактивной
            this._buttonElement.classList.add(this._settings.inactiveButtonClass);
            this._buttonElement.setAttribute('disabled', 'true');
        } else {
            // иначе сделай кнопку активной
            this._buttonElement.classList.remove(this._settings.inactiveButtonClass);
            this._buttonElement.removeAttribute('disabled');
        }
    };

    _hasInvalidInput() {
        // проходим по этому массиву методом some
        return this._inputList.some((inputElement) => {
            // Если поле не валидно, колбэк вернёт true
            // Обход массива прекратится и вся фунцкция
            // hasInvalidInput вернёт true

            return !inputElement.validity.valid;
        })
    };
}

class SigningForm {
    constructor(formSelector, submitCallback) {
        this._formElement = document.querySelector(formSelector);
        this._submitCallback = submitCallback;
    }

    hide() {
        this._formElement.classList.remove('signing-form_active');
    }

    show() {
        this._formElement.classList.add('signing-form_active');
    }

    _getInputValues() {
        this._inputList = this._formElement.querySelectorAll('.signing-form__input');

        // создаём пустой объект
        this._formValues = {};

        // добавляем в этот объект значения всех полей
        this._inputList.forEach(input => {
            this._formValues[input.name] = input.value;
        });

        // возвращаем объект значений
        return this._formValues;
    }

    reset() {
        this._formElement.reset();
    }

    setEventListeners() {
        this._formElement.addEventListener('submit', (evt) => {

            evt.preventDefault();
            this._submitCallback(this._getInputValues());
        })
    }
}

const signupForm = new SigningForm('#signup-form', (values) => {
    const username = values.fullname;
    const email = values.email;
    const firstPass = values.password;
    const secondPass = values.confirmpassword;

    if (confirmedPasswordCheck(firstPass, secondPass)) {
        renderLoader(true);
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
                return res.json()
            }
            else if (res.status !== 200){
                console.log(res.status);
                renderLoader(false);
                return res.json()
            }

        }).then(function (data) {
            if (data['message'] !== 'OK'){
                document.querySelector('#email-error').textContent = data['message'];
            }
        })

        console.log('dsfg');

    }

})

const signinForm = new SigningForm('#signin-form', (values) => {
    const username = values.signinusername;
    const password = values.signinpassword;
    renderLoader(true);
    fetch('/sign_in_check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            userPassword: password
        })
    })

    .then((res) => {

        if (res.status === 200) {
            console.log('You was loged in!');
            renderLoader(false);
            signinForm.reset();

            window.location.href = '/';

        }
        else if (res.status !== 200){
            renderLoader(false);
            console.log(res.status);
            return res.json()
        }

    }).then(function (data) {
        console.log(data.message)
        if (data.message === 'The username is incorrect') {
            document.querySelector('#signinusername-error').textContent = data.message;
        }
        else if (data['message'] === 'The password is incorrect') {
            document.querySelector('#signinpassword-error').textContent = data['message'];
        }

    })
})

const signupFormValidation = new FormValidator({
    inputSelector: '.signing-form__input',
    submitButtonSelector: '.signing-form__submitBtn',
    inactiveButtonClass: 'signing-form__submitBtn_inactive',
    inputErrorClass: 'signing-form__input-error',
}, `#signup-form`);

const signinFormValidation = new FormValidator({
    inputSelector: '.signing-form__input',
    submitButtonSelector: '.signing-form__submitBtn',
    inactiveButtonClass: 'signing-form__submitBtn_inactive',
    inputErrorClass: 'signing-form__input-error',
}, `#signin-form`);

signupFormValidation.enableValidation();
signinFormValidation.enableValidation();

signupForm.setEventListeners();
signinForm.setEventListeners();

signupFormChanger.addEventListener('click', changeModeToIn);
signinFormChanger.addEventListener('click', changeModeToUp);