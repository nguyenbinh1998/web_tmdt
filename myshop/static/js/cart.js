var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        if (user === "AnonymousUser"){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }

    })
}

function updateUserOrder(productId, action){
    url = '/update-item/'
    fetch(url, {
        method: "POST",
        headers:{
            'X-CSRFTOKEN':csrftoken,
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then(response => response.json())
    .then(data => {
        location.reload();
    })
}