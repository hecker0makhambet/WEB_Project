import Api from './API.js'
import CartCard from '../components/CartCard.js'
import PopupWithImage from './PopupImage.js'
let navbarBtns = document.querySelectorAll('.navbar__linktext');
navbarBtns.forEach((btn) => {
    console.log(btn);
    btn.classList.remove('navbar__linktext_active');
}) 
document.querySelector('#navbarCart').classList.add('navbar__linktext_active');


const cartForm = document.querySelector('#cartForm'); 

const totalP = document.querySelector('#total'); 


cartForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const fullname = document.querySelector('#fullname').value; 
    const phone = document.querySelector('#phone').value; 
    const address = document.querySelector('#address').value; 
    cards = document.querySelectorAll('.cardCard_l');
    cards.forEach((card) => {
        let amount = card.querySelector('.cartCard__amount').value;
        let productname = card.querySelector('.cartCard__name').textContent;
        console.log(card.id)
        let price = parseInt(card.querySelector('.cartCard__price').textContent.substring(0, card.querySelector('.cartCard__price').textContent.length - 3).replace(/\s/g, ''));
        fetch('/newOrder', {
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST', 
            body: JSON.stringify({
                toyId: card.id,
                fullname: fullname,
                productname: productname,
                phone: phone,
                address: address,
                amount: amount,
                price: price                
            })
        }).then(() => {
            cartForm.setAttribute('style', 'display: none')
            console.log('dfg')
            window.location.href = '/kaspi';
        })
    })
    bestsellersList.textContent = '';
})

const api = new Api({
    headers: {
        'Content-Type': 'application/json'
    }
});

const imagePopup = new PopupWithImage('#popupImg');
imagePopup.setEventListeners();

const bestsellersList = document.querySelector('#shoppingCart');

let cards = [];

api.getCart().then((resp) => {
    Array.from(resp.toys).forEach((res) => {
        const card = new CartCard({
            id: res.id,
            product_name: res.product_name,
            product_image_name: res.product_image_name,
            measure_unit: res.measure_unit,
            product_price: res.product_price,
            product_description: res.product_description
        },
        '#cartCardTemplate',
        () => {
            imagePopup.open(res.product_name, `/static/images/products/${res.id}/${res.product_image_name}`);
        },
        (id) => {
            api.removeFromCart(id);
            card.delete();
        },
        () => {
            card.plus();
        },
        () => {
            card.minus();
        }
        )
        const toy = card.createPost();
        bestsellersList.append(toy);

    })
    if (Array.from(resp.toys).length === 0) {
        cartForm.setAttribute('style', 'display: none')
    }
    cards = document.querySelectorAll('.cardCard_l');
    countTotal();
    cards.forEach((card) => {
        const plus = card.querySelector('#cartCardPlus');
        const min = card.querySelector('#cartCardMinus');
        const rem = card.querySelector('.cartCard__remove');
        plus.addEventListener('click', countTotal);
        min.addEventListener('click', countTotal);
        rem.addEventListener('click', countTotal);
    })
})

function countTotal() {
    cards = document.querySelectorAll('.cardCard_l');
    let totalPrice = 0;

    cards.forEach((card) => {
        let amount = card.querySelector('.cartCard__amount').value;
        
        let price = parseInt(card.querySelector('.cartCard__price').textContent.substring(0, card.querySelector('.cartCard__price').textContent.length - 3).replace(/\s/g, ''));
        
        totalPrice += amount * price;
    })
    totalP.textContent = 'Total: ' + totalPrice + ' KZT';
}