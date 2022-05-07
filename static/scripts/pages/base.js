const menuBtn = document.querySelector('.navbar__menuBtn');
const navbar = document.querySelector('.navbar');

menuBtn.addEventListener('click', navbarHandler)

isMenuBtnActive = false;

function toggleMenu() {
    if (isMenuBtnActive) {
        isMenuBtnActive = false;
        menuBtn.src = '../static/images/dev/blacknavbarmenu.svg';
    }
    else {
        isMenuBtnActive = true;
        menuBtn.src = '../static/images/dev/navbar__menu.svg';
    }
}

function openNavbar() {
    navbar.classList.toggle('navbar_active');
}

function navbarHandler(e) {
    openNavbar();
    toggleMenu();
}




class Popup {
    constructor(popupSelector) {
        this._popupElement = document.querySelector(popupSelector);
        this._handleEscClose = this._handleEscClose.bind(this);
    }

    _handleEscClose(evt) {
        if (evt.key === 'Escape') {
            this.close();
        }
    }

    _handleOverlayClick(evt) {
        if (evt.target.classList.contains('popup_opened')) {
            this.close();
        }
    }

    open() {
        document.addEventListener('keydown', this._handleEscClose);
        this._popupElement.classList.add("popup_opened");
    }

    close() {
        document.removeEventListener('keydown', this._handleEscClose);
        this._popupElement.classList.remove("popup_opened");
    }

    setEventListeners() {
        this._popupCloseBtn = this._popupElement.querySelector('.popup__close');
        this._popupCloseBtn.addEventListener('click', () => {
            this.close();
        });
        this._popupElement.addEventListener('click', this._handleOverlayClick.bind(this));
    }
};

class PopupWithImage extends Popup {
    constructor(popupSelector) {
        super(popupSelector);
        this._imgPopupImg = this._popupElement.querySelector(".popup__image");
        this._imgPopupTitle = this._popupElement.querySelector(".popup__title");
    }

    open(title, url) {
        this._imgPopupImg.src = url;
        this._imgPopupImg.alt = title;
        this._imgPopupTitle.textContent = title;
        super.open();
    }
}

const imagePopup = new PopupWithImage('#popupImg');
imagePopup.setEventListeners();

if (document.querySelector('.user__image')) {
    document.querySelector('.user__image').addEventListener('click', () => {
        if ((window.location.href).includes('profile/')) {
            const trash = document.createElement('img');
            trash.src = '/static/images/dev/trash.svg';
            trash.alt = 'trash';
            trash.classList.add('popup__trash');

            trash.addEventListener('click', (e) => {
                const username = e.target.parentElement.querySelector('.popup__image').alt;
                renderLoader(true);
                fetch('/delete_avatar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: username
                        
                    })
                }).then((res) => {
                    if (res.ok) {
                        location.href = '/profile/'
                    }
                    else if (res.status !== 200){
                        console.log(res.status);
                        
                    }
            
                })
            })
            document.querySelector('.popup__img-container').append(trash);
        }
        imagePopup.open(document.querySelector('.user__name').textContent, document.querySelector('.user__image').src);
    })
}