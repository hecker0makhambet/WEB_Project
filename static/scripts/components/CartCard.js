// import dastan from '../utils/constants.js';

export default class CartCard {
    constructor(data, selectorTemplate, handleCardClick, handleRemoveFromCartClick, handlePlusClick, handleMinusClick) {
        this._id = data.id;
        
        this._product_name = data.product_name;
        this._product_image_name = data.product_image_name;
        
        this._measure_unit = data.measure_unit;
        this._product_price = data.product_price;
        this._product_description = data.product_description;
        
        this._handleCardClick = handleCardClick;
        this._handleRemoveFromCartClick = handleRemoveFromCartClick;
        this._handleMinusClick = handleMinusClick;
        this._handlePlusClick = handlePlusClick;

        this._selectorTemplate = selectorTemplate;

        this._mainImgDir = `/static/images/products/${this._id}/${this._product_image_name}`

    }

    _getTemplate() {
        return document.querySelector(this._selectorTemplate).content.cloneNode(true);
    }

    createPost() {
        const card = this._getTemplate();
        this._img = card.querySelector(".cartCard__image");
        
        
        this._cardDescription = card.querySelector('.cartCard__description');
        this._cardName = card.querySelector('.cartCard__name');
        this._cardPrice = card.querySelector('.cartCard__price');

        this._elemCard = card.querySelector('.cartCard');
        this._elemCard.classList.add('cardCard_l');
        this._elemCard.id = this._id;
        this._amount = card.querySelector('.cartCard__amount');

        this._removeBtn = card.querySelector('.cartCard__remove');
        this._plusBtn = card.querySelector('#cartCardPlus');
        this._minusBtn = card.querySelector('#cartCardMinus');

        this._img.src = this._mainImgDir;
        this._img.alt = this._product_name;

        this._cardName.textContent = this._product_name;
        this._cardDescription.textContent = this._product_description.substring(0, 50) + '...';
        this._cardPrice.textContent = `${this._product_price} KZT`;
            
        this._setEventListeners();
        return card;
    }

    _setEventListeners() {
        this._img.addEventListener('click', (e) => {
            this._handleCardClick();
        });

        this._plusBtn.addEventListener('click', () => {
            this._handlePlusClick();
        })

        this._minusBtn.addEventListener('click', () => {
            this._handleMinusClick();
        })

        this._removeBtn.addEventListener('click', () => {
            this._handleRemoveFromCartClick(this._id);
        })
    }

    plus() {
        this._amount.value = parseInt(this._amount.value) + 1;
    }

    minus() {
        if (parseInt(this._amount.value) > 0) {
            this._amount.value = parseInt(this._amount.value) - 1;
        }
        
    }

    delete() {
        this._elemCard.remove();
    }

}