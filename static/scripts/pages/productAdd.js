import Api from './API.js'

const api = new Api({
    headers: {
        'Content-Type': 'application/json'
    }
});

const newProductForm = document.querySelector('#new-product-form');
const product_name = document.querySelector('#productname');
const category = document.querySelector('#category');
const country = document.querySelector('#country');
const company = document.querySelector('#company');
const price = document.querySelector('#price');
const quantity_in_stock = document.querySelector('#quantity_in_stock');
const product_description = document.querySelector('#product_description');
const product_gender = document.querySelector('#product_gender');
const age = document.querySelector('#age');
const measure_unit = document.querySelector('#measure_unit');

newProductForm.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log('mama')
    api.newProduct(
        product_name.value,
        category.value,
        price.value,
        country.value,
        company.value,
        quantity_in_stock.value,
        product_description.value,
        product_gender.value,
        age.value,
        measure_unit.value
        ).then((data) => {
            console.log(data.idP);
            document.querySelector('#prodid').value = data.idP;
        })
})