import Popup from './Popup.js'

export default class PopupWithImage extends Popup {
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