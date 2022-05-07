export default class Popup {
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
