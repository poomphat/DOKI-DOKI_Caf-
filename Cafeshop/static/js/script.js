$(document).ready(cartList());

function openorder() {
    orderside = document.getElementById('order');
    orderside.style.transition = "ease 0.55s";
    //console.log(orderside.style.right);
    if (orderside.style.right == '-100%' || orderside.style.right == '') {
        orderside.style.right = "0%";
    } else {
        orderside.style.right = "-100%";
    }
}

total_price = 0

function cartList() {
    clearCart()
    var cart = []
    if (Cookies.get('cart') !== undefined) {
        cart = JSON.parse(Cookies.get('cart'))
    }
    tablecart = document.getElementById('cart')
    if (cart.length > 0) {
        openCart()
    }
    for (var i = 0; i < cart.length; i++) {
        tr = document.createElement('tr')
        tr.className = 'cartItem'
        tr.dataset.pos = i
        td = document.createElement('td')
        td.innerText = i + 1
        tr.appendChild(td)
        td = document.createElement('td')
        p = document.createElement('p')
        if (cart[i].kind == 'coffee') {
            p.innerHTML = cart[i].name + '(' + cart[i].type + ')'
            td.appendChild(p)
            hr = document.createElement('hr')
            td.appendChild(hr)
            ul = document.createElement('ul')
            li = document.createElement('li')
            var sweetness_name = {
                'normalsweet': 'หวานปกติ',
                'lesssweet': 'หวานน้อย',
                'moresweet': 'หวานมาก',
            }
            li.innerHTML = sweetness_name[cart[i].sweetness]
            ul.appendChild(li)
            td.appendChild(ul)
        } else if (cart[i].kind == 'juice') {
            p.innerHTML = cart[i].name
            td.appendChild(p)
            hr = document.createElement('hr')
            td.appendChild(hr)
            ul = document.createElement('ul')
            for (var j = 0; j < cart[i].fruit.length; j++) {
                li = document.createElement('li')
                li.innerHTML = cart[i].fruit[j].name
                ul.appendChild(li)
                td.appendChild(ul)
            }
        }
        if (cart[i].topping_list.length > 0) {
            hr = document.createElement('hr')
            td.appendChild(hr)
            ul = document.createElement('ul')
            for (var j = 0; j < cart[i].topping_list.length; j++) {
                li = document.createElement('li')
                li.innerHTML = cart[i].topping_list[j].name + '(' + cart[i].topping_list[j].amount + ')'
                ul.appendChild(li)
                td.appendChild(ul)
            }
            td.appendChild(ul)
        }
        hr = document.createElement('hr')
        td.appendChild(hr)
        p = document.createElement('p')
        p.innerText = 'จำนวน :  '
        input = document.createElement('input')
        input.setAttribute("type", "number");
        input.setAttribute("min", "1");
        input.setAttribute("id", 'item-' + i + '-amount')
        input.dataset.pos = i
        input.value = cart[i].amount
        input.style.width = '10vw'
        input.oninput = function(event) {
            pos = Number(event.target.dataset.pos)
            cart[pos].amount = event.target.value
            Cookies.set('cart', JSON.stringify(cart))
            calCartPrize()
        }
        input.onkeyup = function() {
            input.value = input.value.replace(/[^\d]/, '')
        }
        p.appendChild(input)
        td.appendChild(p)
        hr = document.createElement('hr')
        td.appendChild(hr)
        p = document.createElement('p')
        p.innerText = 'ราคา : '
        span = document.createElement('span')
        span.className = 'item-' + i + '-price'
        span.innerText = cart[i].price_incTopping
        p.appendChild(span)
        td.appendChild(p)
        td.appendChild(document.createElement('hr'))
        button = document.createElement('button')
        button.className = 'btn btn-danger'
        button.setAttribute("type", "button")
        button.innerText = 'ลบรายการ'
        button.dataset.pos = i
        button.onclick = function(event) {
            cart.splice(event.target.dataset.pos, 1)
            Cookies.set('cart', JSON.stringify(cart))
            cartList()
        }
        td.appendChild(button)
        tr.appendChild(td)
        tablecart.appendChild(tr)

    }
    calCartPrize()
}

function clearCart() {
    document.querySelectorAll('.cartItem').forEach(el => el.remove());
    total_price = 0;
    document.getElementById('ordered').style.display = 'none';
    document.getElementById('unordered').style.display = '';
}

function openCart() {
    document.getElementById('ordered').style.display = '';
    document.getElementById('unordered').style.display = 'none';
}

function changeDrinkPrice(price) {
    priceAll = document.getElementsByClassName('DrinkPrice')
    for (var i = 0; i < priceAll.length; i++) {
        priceAll[i].innerText = price
    }
}

function calCartPrize() {
    var cart = []
    if (Cookies.get('cart') !== undefined) {
        cart = JSON.parse(Cookies.get('cart'))
    }
    var total_cart_price = 0
    for (var i = 0; i < cart.length; i++) {
        total_cart_price += cart[i].amount * cart[i].price_incTopping
        order.total_price = total_cart_price
    }
    axios.post('/api_promotion/', {
        id: document.getElementById('promotion').value
    }).then(function(response) {
        for(var i=0;i<cart.length;i++){
            total_cart_price = total_cart_price - (response.data.discount * cart[i].amount)
        }
        //console.log(total_cart_price)
        if(Number(total_cart_price)<0){
            total_cart_price = 0
        }
        document.getElementById('cartTotalPrice').innerText = total_cart_price
        total_price = total_cart_price
        console.log(response)
    }).catch(function(error) {
        console.log(error)
    });
    document.getElementById('cartTotalPrice').innerText = total_cart_price
}

function makeorder() {
    order = {
        cart: '',
        total_price: 0,
        promotion: 0,
    }
    order.cart = JSON.parse(Cookies.get('cart'))
    order.promotion = Number(document.getElementById('promotion').value)
    order.total_price = total_price

    var x = axios.post('/api/', {
        order: order
    }).then(function(response) {
        Cookies.remove('cart')
        console.log(response)
        return response
    }).catch(function(error) {
        console.log(error)
    });

    clearCart()
    cart = Array()

}
