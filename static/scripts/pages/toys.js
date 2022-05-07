import Api from './API.js'
import Card from '../components/Card.js'
import PopupWithImage from './PopupImage.js'
let navbarBtns = document.querySelectorAll('.navbar__linktext');
navbarBtns.forEach((btn) => {
    console.log(btn);
    btn.classList.remove('navbar__linktext_active');
}) 
document.querySelector('#navbarToys').classList.add('navbar__linktext_active');
const api = new Api({
    headers: {
        'Content-Type': 'application/json'
    }
});

const imagePopup = new PopupWithImage('#popupImg');
imagePopup.setEventListeners();

const bestsellersList = document.querySelector('#bestsellers');

api.getListOfBestsellers().then((resp) => {
    console.log('myau')
    Array.from(resp.toys).forEach((res) => {
        const card = new Card({
            id: res.id,
            product_name: res.product_name,
            product_image_name: res.product_image_name,
            category: res.category,
            country: res.country,
            quantity_in_stock: res.quantity_in_stock,
            product_rating: res.product_rating,
            product_gender: res.product_gender,
            measure_unit: res.measure_unit,
            product_price: res.product_price,
            age: res.age,
            isLiked: res.isLiked
        },
        '#cardTemplate',
        () => {
            imagePopup.open(res.product_name, `/static/images/products/${res.id}/${res.product_image_name}`);
        },
        (id) => {
            api.addToCart(id).then((res) => {
                if (res.message === "Signin") {
                    window.location.href = '/signing/'
                }
            });
        },
        (id, isLiked) => {
            api.like(id, isLiked).then((data) => {
                if (data.message === "Signin") {
                    window.location.href = '/signing/'
                }
                else {
                    card.like(data.isLiked);
                }
                
            })
            
        },
        api.isLiked(res.id).then((data) => {
            return data.isLiked
            
        })
        )
        const toy = card.createPost();
        bestsellersList.append(toy);

    })
    
})