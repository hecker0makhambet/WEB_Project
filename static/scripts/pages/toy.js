import Api from './API.js';

const api = new Api({
    headers: {
        'Content-Type': 'application/json'
    }
});

document.querySelector('.userdata__submitBtn').addEventListener('click', () => {
    api.addToCart(document.querySelector('#toyid').textContent).then((res) => {
        if (res.message === "Signin") {
            window.location.href = '/signing/'
        }
    });
})