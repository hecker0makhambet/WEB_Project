// import dastan from '../utils/constants.js';

export default class Card {
    constructor(data, selectorTemplate, handleCardClick, handleAddtoCartClick, handleLikeClick, isLiked) {
        this._id = data.id;
        
        this._product_name = data.product_name;
        this._product_image_name = data.product_image_name;
        this._category = data.category;
        this._country = data.country;
        this._company = data.company;
        this._quantity_in_stock = data.quantity_in_stock;
        this._product_rating = data.product_rating;
        this._product_gender = data.product_gender;
        this._measure_unit = data.measure_unit;
        this._product_price = data.product_price;
        this._age = data.age;
        isLiked.then((data) => {
            if (data){
                this._likeBtn.classList.add('card__like_active')
            }
            else {
                this._likeBtn.classList.remove('card__like_active');
            }
        })
        this._handleCardClick = handleCardClick;
        this._handleAddtoCartClick = handleAddtoCartClick;
        this._handleLikeClick = handleLikeClick;
        this._selectorTemplate = selectorTemplate;

        this._mainImgDir = `/static/images/products/${this._id}/${this._product_image_name}`

    }

    _getTemplate() {
        return document.querySelector(this._selectorTemplate).content.cloneNode(true);
    }

    createPost() {
        const card = this._getTemplate();
        this._img = card.querySelector(".card__image");
        
        this._likeBtn = card.querySelector(".card__like");
        
        this._cardName = card.querySelector('.card__name');
        this._cardPrice = card.querySelector('.card__price');

        this._elemCard = card.querySelector('.card');

        this._addCard = card.querySelector('#addCardBtn');
        this._moreCard = card.querySelector('#more');

        this._img.src = this._mainImgDir;
        this._img.alt = this._product_name;

        this._cardName.textContent = this._product_name;
        this._cardPrice.textContent = `${this._product_price} KZT`;

        this._moreCard.href = `/toy/${this._id}`
        
        
            
        this._setEventListeners();
        return card;
    }

    _setEventListeners() {
        this._img.addEventListener('click', (e) => {
            this._handleCardClick();
        });
        this._likeBtn.addEventListener('click', () => {
            this._likeBtn.classList.toggle('card__like_active');
            this._handleLikeClick(this._id, this._likeBtn.classList.contains('card__like_active'));
        })
        this._addCard.addEventListener('click', () => {
            this._handleAddtoCartClick(this._id);
        })
    }

    delete() {
        this._elemCard.remove();
    }

    like(isLiked) {
        console.log('МЯУ');
        if (isLiked) {
            this._likeBtn.classList.add('card__like_active');
        }
        else {
            this._likeBtn.classList.remove('card__like_active');
        }
    }

}