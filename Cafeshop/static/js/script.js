var name = ''
    var drink_id = ''
    var drink_type = ''
    var drink_price = ''
    var drink_kind = ''
    var sweetness = ''
    var topping_list = Array()
    var cart = Array()
    var total_cart_price = 0
    var sweetness_name = {
        'normalsweet': 'หวานปกติ',
        'lesssweet': 'หวานน้อย',
        'moresweet': 'หวานมาก',
    }
    var fruit = Array()
    function openorder() {
        orderside = document.getElementById('order');
        orderside.style.transition = "ease 0.55s";
        console.log(orderside.style.right);
        if (orderside.style.right == '-100%' || orderside.style.right == '') {
            orderside.style.right = "0%";
        } else {
            orderside.style.right = "-100%";
        }
    }
    function deleteMenu() {
        document.querySelectorAll('.menu').forEach(el => el.remove());
    }

    function deleteAllTopping() {
        document.querySelectorAll('.addTopping').forEach(el => el.remove());
    }

    function addToCart() {
        if (!drink_id == '') {
            addtoppingElement = document.querySelectorAll('.addTopping')
            var temp_price = 0
            for (var i = 0; i < addtoppingElement.length; i++) {
                first = addtoppingElement[i].firstElementChild
                price = Number(first.options[first.selectedIndex].dataset.price)
                id = first.options[first.selectedIndex].value
                name = first.options[first.selectedIndex].innerText
                next = first.nextElementSibling
                amount = Number(next.value)
                temp_price += Number(price) * amount
                topping_list.push({
                    id: id,
                    name: name,
                    price: price,
                    amount: amount
                })

            }
            var drink = {
                id: drink_id,
                name: drink_name,
                type: drink_type,
                kind: drink_kind,
                sweetness: sweetness,
                price: drink_price,
                amount: 1,
                price_incTopping: temp_price + drink_price,
                fruit: fruit,
                topping_list: topping_list
            }
            cart.push(drink)
            $('.bd-example-modal-xl-coffee').modal('hide')
            $('.bd-example-modal-xl-smoothie').modal('hide')
            reset()
            cartList()
            document.getElementById('nonDrinkAddtoCard').style.display = '';
            document.getElementById('ordered').style.display = '';
            document.getElementById('unordered').style.display = 'none';
        } else {
            document.getElementById('nonDrinkAddtoCard').style.display = 'inline';
        }

    }

    function clearallcoffee() {
        var O = document.querySelectorAll('.btncool');
        for (var i = 0; i < O.length; i++) {
            O[i].style.background = "#EFEFEF";
            O[i].style.color = "black";
        }
    }

    function selectThis(event) {

        target = event.target.parentNode
        target = target.firstElementChild

        drink_name = target.innerText
        target = target.nextElementSibling
        drink_id = Number(target.innerText)
        target = target.nextSibling
        drink_type = target.innerText
        target = target.nextSibling
        drink_price = Number(target.innerText)
        drink_kind = 'coffee'

        sweet_select = document.getElementsByClassName('sweetness')[0]
        sweetness = sweet_select.options[sweet_select.selectedIndex].value
        changeDrinkPrice(drink_price)
        clearallcoffee()
        event.target.style.background = "#44D362";
        event.target.style.color = "white";
    }

    function recalDrinkPrice(event) {
        addtoppingElement = document.querySelectorAll('.addTopping')
        var temp_price = 0
        for (var i = 0; i < addtoppingElement.length; i++) {
            first = addtoppingElement[i].firstElementChild
            price = first.options[first.selectedIndex].dataset.price
            next = first.nextElementSibling
            price = Number(price) * Number(next.value)
            temp_price += price

        }
        changeDrinkPrice(drink_price + temp_price)
    }

    function reset() {
        deleteMenu()
        deleteAllTopping()
        changeDrinkPrice(0)
        clearallcoffee()
        drink_name = ''
        drink_id = ''
        drink_type = ''
        drink_price = ''
        sweetness = ''
        drink_kind = ''
        topping_list = Array()
        fruit = Array()

    }

    function changeSweet(event) {
        var select = event.target
        var option = select.options[select.selectedIndex]
        sweetness = select.options[select.selectedIndex].value
    }

    function cartList() {
        clearCart()
        tablecart = document.getElementById('cart')
        for (var i = 0; i < cart.length; i++) {
            tr = document.createElement('tr')
            tr.className = 'cartItem'
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
            p.innerText = 'จำนวน : '
            span = document.createElement('span')
            span.className = 'item-'+i+'-amount'
            span.innerText = cart[i].amount
            p.appendChild(span)
            td.appendChild(p)
            hr = document.createElement('hr')
            td.appendChild(hr)
            p = document.createElement('p')
            p.innerText = 'ราคา : '
            span = document.createElement('span')
            span.className = 'item-'+i+'-price'
            span.innerText = cart[i].amount * cart[i].price_incTopping
            p.appendChild(span)
            td.appendChild(p)
            tr.appendChild(td)
            tablecart.appendChild(tr)
            calCartPrize()

        }

    }

    function clearCart() {
        document.querySelectorAll('.cartItem').forEach(el => el.remove());
        total_cart_price = 0;
        document.getElementById('ordered').style.display = 'none';
        document.getElementById('unordered').style.display = '';
    }

    function checkMT5(event) {
        if (Number(event.target.value) > 5) {
            event.target.value = 5;
        }
    }

    function selectFruitThis(event) {

        target = event.target
        drink_name = 'Juice'
        drink_id = 8
        drink_kind = 'juice'
        drink_price = 45
        if (!(fruit.some(f => f.id == target.dataset.id))) {
            fruit.push({

                id: target.dataset.id,
                name: target.innerText

            })
            target.style.background = "#44D362";
            target.style.color = "white";
        } else {
            fruit = fruit.filter(f => f.id !== target.dataset.id)
            target.style.background = "#EFEFEF";
            target.style.color = "black";
        }
    }

    function changeDrinkPrice(price) {
        priceAll = document.getElementsByClassName('DrinkPrice')
        for (var i = 0; i < priceAll.length; i++) {
            priceAll[i].innerText = price
        }
    }
    function calCartPrize(){
        total_cart_price = 0
        for (var i = 0; i < cart.length; i++){
            total_cart_price += cart[i].amount * cart[i].price_incTopping
        }
        document.getElementById('cartTotalPrice').innerText = total_cart_price
    }
    function order(){
        var order = {
            cart : cart,
            total_price : total_cart_price,
        }
        clearCart()
        reset()
        cart = Array()
        axios.post('api/', {
            order:order}
        ).then(function (response){
            console.log(response)
        }).catch(function (error){
            console.log(error)
        });

        
    }
