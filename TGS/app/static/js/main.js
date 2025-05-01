

$('.plus-cart').click(function(){
    var id =$(this).attr("data-pid").toString();
    var eml =(this.parentNode.children[2])
    console.log("pid =",id)
    $.ajax({
        type: "GET",
        url:"/pluscart",
        data:{
            prod_id : id
        },
        success: function(data){
            console.log("data = ",data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            
        }
    })
})

$('.minus-cart').click(function(){
    var id =$(this).attr("data-pid").toString();
    var eml =(this.parentNode.children[2])
    console.log("pid =",id)
    $.ajax({
        type: "GET",
        url:"/minuscart",
        data:{
            prod_id : id
        },
        success: function(data){
            console.log("data = ",data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})


$('.remove-cart').click(function(){
    var id =$(this).attr("data-pid").toString();
    var eml =this
    $.ajax({
        type: "GET",
        url:"/removecart",
        data:{
            prod_id : id
        },
        success: function(data){
            console.log("data = ",data);
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})

$('.plus-wishlist').click(function(){
    var id =$(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url:"/wishlist/add",
        data:{
            prod_id : id
        },
        success: function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

$('.minus-wishlist').click(function(){
    var id =$(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url:"/wishlist/remove",
        data:{
            prod_id : id
        },
        success: function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})
