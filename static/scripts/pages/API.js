
export default class Api {
    constructor(options) {
        this.headers = options['headers'];
    }

    handleOriginalResponse = (res) => {
        if (!res.ok) {
          return Promise.reject(`Error: ${res.status}`);
        }
        return res.json();
      }
      
    newProduct(product_name, category, price, country, company, quantity_in_stock, product_description, product_gender, age, measure_unit) {
        return fetch('/add_product/', {
            headers: this.headers,
            method: "POST",
            body: JSON.stringify({
                price: price,
                product_name: product_name,
                category: category,
                country: country,
                company: company,
                quantity_in_stock: quantity_in_stock,
                product_description: product_description,
                product_gender: product_gender,
                age: age,
                measure_unit: measure_unit
            })
        })
            .then(this.handleOriginalResponse);
    }

    getListOfBestsellers(){
        return fetch('/get_bestsellers/', {
            headers: this.headers,
            method: "GET"
        }).then(this.handleOriginalResponse);
    }

    getLiked(){
        return fetch('/getLiked/', {
            headers: this.headers,
            method: "GET"
        }).then(this.handleOriginalResponse);
    }

    getCart(){
        return fetch('/getCart/', {
            headers: this.headers,
            method: "GET"
        }).then(this.handleOriginalResponse);
    }

    removeFromCart(id) {
        return fetch('/removeFromCart/', {
            headers: this.headers,
            method: "POST",
            body: JSON.stringify({
                cardId: id
            })
        })
            .then(this.handleOriginalResponse);
    }

    addToCart(id) {
        return fetch('/addToCart/', {
            headers: this.headers,
            method: "POST",
            body: JSON.stringify({
                cardId: id
            })
        })
            .then(this.handleOriginalResponse);
    }

    like(id, isLiked) {
        return fetch('/cardLike/', {
            headers: this.headers,
            method: "POST",
            body: JSON.stringify({
                cardId: id,
                isLiked: isLiked
            })
        })
            .then(this.handleOriginalResponse);
    }

    isLiked(id) {
        return fetch('/checkForLiked/', {
            headers: this.headers,
            method: "POST",
            body: JSON.stringify({
                cardId: id
            })
        })
            .then(this.handleOriginalResponse);
    }
}