{% extends 'users/base.html' %} {% load static %} {% block index %}

<div class="container p-5 bg-white border">
  <div class="row">
    <div class="col-md-4">
      <h2>order summery</h2>
      {% for item in items %}
      <div class="d-flex my-3">
        <div class="px-4 py-3 bg-white border">
          <img src="{{ item.product.images1.url }}" alt="" style="max-width: 80px" />
        </div>
        <div class="ml-4 mt-4 pl-2">
          <h4>{{ item }}</h4>
          <h5>
            {{ item.product.ram }} |<br />
            {{ item.product.storage }}
          </h5>
          <h4 class="mb-4">₹{{ item.product.price }}</h4>
          <span>Total </span>
          <h4>₹{{ item.get_total }}</h4>
        </div>
      </div>
      {% endfor %}
      <span>Order Total </span>
      <h3>₹{{ order.get_cart_total }}</h3>
    </div>
    <div class="col-md-8 bg-white border pb-3">
      <div class="col-md-12 border border-dark my-4">
        {% if address %}
        <div class="col-12 text-center mt-3">
          <h3>SELECT SHIPPING ADDRESS</h3>
        </div>
        {% else %}
        <div class="col-12 text-center mt-3 text-secondary">
          <h3>ADD SHIPPING ADDRESS</h3>
        </div>
        {% endif %}
        <div class="row m-0">
          {% for address in address %}
          <div class="col-md-6 my-3">
            <div class="col-md-12 border border-success" id="{{ address.id }}">
              <table>
                <tr>
                  <td></td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td>
                    <input type="radio" name="address" value="{{ address.id }}" />
                  </td>
                  <td></td>
                  <td></td>
                </tr>
                <tr>
                  <td>NAME</td>
                  <td>:</td>
                  <td>{{ address.name }}</td>
                </tr>
                <tr style="vertical-align: top">
                  <td class="pr-3 sticky-top">ADDRESS</td>
                  <td class="pr-3">:</td>
                  <td>
                    <div style="white-space: pre-line">
                      {{ address.address }}
                    </div>
                  </td>
                </tr>
                <tr>
                  <td>CITY</td>
                  <td>:</td>
                  <td>{{ address.city }}</td>
                </tr>
                <tr>
                  <td>STATE</td>
                  <td>:</td>
                  <td>{{ address.state }}</td>
                </tr>
                <tr>
                  <td>PIN CODE</td>
                  <td>:</td>
                  <td>{{ address.pincode }}</td>
                </tr>
                <tr>
                  <td>PHONE</td>
                  <td>:</td>
                  <td>{{ address.number }}</td>
                </tr>
              </table>
            </div>
          </div>
          
          {% endfor %}
        </div>
      </div>
      <center>
        <a href="{% url 'add_address' %}"><button class="btn btn-info btn-lg col-md-9">
            &#10010; Add New Address
          </button></a>
      </center>
      <center>
        <div class="col-md-12 d-flex justify-content-between mt-5">
          <div class="col-md-6 pl-0">
            <center>
              <div class="col-md-11 border-danger py-3 border selected">
                <p class="h4 text-secondary">select your address</p>
              </div>
            </center>
          </div>
          <div class="col-md-6 pr-0">
            <center>
              <div class="col-md-11 py-3 border-secondary border">
                <h4>SELECT PAYMENT METHOD</h4>
                <div class="text-left pl-3">
                  <input class="mb-2" type="radio" name="payment" id="RazorPay" value="RazorPay" />
                  RazorPay <br />
                  <div class="d-none" id="div_RazorPay"><button id="rzp-button1">Pay</button></div>
                  <input class="mb-2" type="radio" name="payment" id="PayPal" value="PayPal" />
                  PayPal <br />
                  <div class="d-none" id="div_PayPal">
                    <div id="paypal-button-container"></div>
                  </div>
                  <input class="mb-2" type="radio" name="payment" id="COD" value="COD" />
                  COD <br />
                  <div class="d-none" id="div_COD">
                    <button class="col-md-11 btn btn-lg btn-info mt-4" id="proceed">
                      Proceed
                    </button>
                  </div>
                </div>
              </div>
              <a href="{% url 'add_to_cart' %}"><button class="col-md-12 btn btn-lg btn-warning mt-5" id="cancel">
                  Back to Cart
                </button></a>
            </center>
          </div>
        </div>
      </center>
    </div>
  </div>
</div>


















<div class="m-1">
  <h5 class="m-1">Items:   {{order.get_cart_item}}</h5>
  <h5 class="m-1 " id="b_offer">Total:   <i class="fas fa-rupee-sign"  ></i>{{order.get_cart_total}}</h5>
  <div class=" d-none" id="old_price">
      <div class="d-flex">
          <h6 class="m-1 "><del> Total:   <i class="fas fa-rupee-sign"></i><span id="old_price_val"></span></del></h6>
          <h6 class="m-1 text-success">- <span id="a_offer_percent" >20</span>%</h6>
      </div>    
  </div>
  <h5 class="m-1 d-none" id="a_offer">Total:   <i class="fas fa-rupee-sign"></i> <span id="a_offer_val"> {{order.get_cart_total}} </span> </h5>
  <p class="text-success d-none coupon-success" >*coupon applied</p>
  <div class="">
  {% if order.coupon_used %}
  <p class="text-success  coupon-success" >*coupon applied</p>
  {% endif %}

  </div>
  
  
</div>
{% if order.coupon_used == False %}
<div class="m-2" style="position: relative;">
  <button class="btn btn-success m-1" id="coupon_ask_btn">Use Coupon</button>
  <div class="coupon_apply d-none  bg-light"  style="width: 100%; height: 100%;">
      <div id="coupon-form "  class="d-flex">
          <input type="text" id="input_code" name="coupon_code" value="" required>
          <button class="btn btn-primary" id="coupon_submit_btnn">Apply</button>
      </div>
      <div text-danger id="error"></div>
  </div>
</div>
{% endif %}

























{% extends 'adminbase.html' %}

{% block title%}
<!-- semantic UI -->
<link rel="stylesheet" type='text/css' href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.14/semantic.min.css">
<!--Chart js-->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" integrity="sha256-Uv9BNBucvCPipKQ2NS9wYpJmi8DTOEfTA/nH2aoJALw=" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.css" integrity="sha256-aa0xaJgmK/X74WM224KMQeNQC2xYKwlAt08oZqjeF0E=" crossorigin="anonymous" />
<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
{% endblock title %}

{% block content %}
{% load static %}
<div class="dash-body container " width="100" style="height: 100rem;">
  <main class="main users chart-page" id="skip-target">
    <div class="container">
      <h2 class="main-title">Dashboard</h2>
      <div class="row stat-cards">
        <div class="col-md-6 col-xl-3">
          <article class="stat-cards-item">
            <div class="stat-cards-icon primary">
              <i data-feather="bar-chart-2" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">{{customers}}</p>
              <p class="stat-cards-info__title">Total Customers</p>
             
            </div>
          </article>
        </div>
        <div class="col-md-6 col-xl-3">
          <article class="stat-cards-item">
            <div class="stat-cards-icon warning">
              <i data-feather="file" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">{{orders}}</p>
              <p class="stat-cards-info__title">Total Orders</p>
              
            </div>
          </article>
        </div>
        <div class="col-md-6 col-xl-3">
          <article class="stat-cards-item">
            <div class="stat-cards-icon purple">
              <i data-feather="file" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">{{product_count}}</p>
              <p class="stat-cards-info__title">Total Products</p>
              
            </div>
          </article>
        </div>
        <div class="col-md-6 col-xl-3">
          <article class="stat-cards-item">
            <div class="stat-cards-icon success">
              <i data-feather="feather" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info_num">{{total_revenue.total_amount_sum}}</p>
              <p class="stat-cards-info__title">Total Income</p>
              
            </div>
          </article>
        </div>
      </div>
    </div>
  </main>
     <div class="row p-2">
         <div class="col-md-6 text-center">
           <h2 class="main-title">Products Available</h2>
            <canvas id="productchart" width="400" height="400">

            </canvas> 

         </div>
         <div class="col-md-6 text-center">
          <h2 class="main-title">Order Status</h2>
            <canvas id="orderchart" width="400" height="400">

            </canvas> 

         </div>
         <div class="col-md-6 text-center">
          <h2 class="main-title">Payment Methods</h2>
            <canvas id="paymentchart" width="400" height="400">

            </canvas> 

         </div>
        
       <div class="col-md-6 text-center">
        <h2 class="main-title">Category Wise Orders</h2>
        <canvas id="orderbycategory" width="400" height="400">

        </canvas> 

     </div>
     </div>
</div>
   
 
{% endblock content %}
{% block scripts%}
<script>

$(document).ready(function(){
     const ctx = document.getElementById('productchart').getContext('2d');
     
  
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        
        labels: [{% for product in products %} , '{{product.product_name}}', {% endfor %}],
        datasets: [{
            label: '# numbers',
            data: [{% for product in products %} ,'{{product.quantity_available}}', {% endfor %}],
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

});



</script>

    
<script>
    var xValues = ['placed','shipped','out of delivery','completed','cancelled','returned'];
    var yValues = {{order_status | safe}};
    var barColors = [
    'rgba(255, 159, 64, 0.8)',
    'rgba(255, 99, 132, 0.8)',
    '#77DD77',
    'rgba(54, 162, 235, 0.8)',

    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    

    ];
    
    new Chart("orderchart", {
      type: "pie",
      data: {
        labels: xValues,
        datasets: [{
          backgroundColor: barColors,
          data: yValues
        }]
      },
      options: {
        title: {
          display: true,
          text: "Order Status Chart"
        }
      }
    });
    </script>
    
    <script>
        var xValues = ["Cash On Delevery", "PayPal", "RazorPay"];
        var yValues = {{payment_type}};
        var barColors = [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        ];
        
        new Chart("paymentchart", {
          type: "doughnut",
          data: {
            labels: xValues,
            datasets: [{
              backgroundColor: barColors,
              data: yValues
            }]
          },
          options: {
            title: {
              display: true,
              text: "Payment Modes Chart"
            }
          }
        });
        </script>
 
  
<script>
  var xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
  var yValues = [55, 49, 44, 24, 15];
  var barColors = ["red", "green","blue","orange","brown"];
  
  new Chart("orderbycategory", {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "World Wine Production 2018"
      }
    }
  });
  </script>
  
  
        
{% endblock scripts %}

<!-- Include the PayPal JavaScript SDK -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script
  src="https://www.paypal.com/sdk/js?client-id=AVdP_3k31kUPShXkWZcgyalyo1_QxK33_1RAOAndr51s9S0_Y6tQKEHXuMR_qyF5PpY1QVE63WNy7gLO&currency=USD"></script>
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script src="https://unpkg.com/sweetalert/dist/sweetalert.min.js"></script>

<script>
  // Render the PayPal button into #paypal-button-container
  var rs_in = parseFloat('{{ order.get_cart_total }}')
  var total_usd = rs_in / 75
  paypal
    .Buttons({
      // Set up the transaction
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [
            {
              amount: {
                value: parseFloat(total_usd).toFixed(2),
              },
            },
          ],
        });
      },

      // Finalize the transaction
      onApprove: function (data, actions) {
        return actions.order.capture().then(function (orderData) {
          console.log(
            "Capture result",
            orderData,
            JSON.stringify(orderData, null, 2)
          );
          order_place();
        });
      },
    })
    .render("#paypal-button-container");
</script>

<script data-namespace="paypal_sdk" src="https://www.paypal.com/sdk/js?client-id=AVn8MVh5G2abs9bvuq3gr7L_wojUYyv4anPw7O5cJVzhItv_WF8cUlom3yiVZtRpJRDuw6UTqzIUV1Lz&currency=USD"></script>
<script>
    var total_amount = parseFloat('{{order.get_cart_total}}')
    var inr_total = total_amount/75
    paypal_sdk.Buttons({

      // Sets up the transaction when a payment button is clicked
      createOrder: function(data, actions) {
        return actions.order.create({
          purchase_units: [{
            amount: {
              value: inr_total.toFixed(2) // Can reference variables or functions. Example: `value: document.getElementById('...').value`
            }
          }]
        });
      },

      // Finalize the transaction after payer approval
      onApprove: function(data, actions) {
        return actions.order.capture().then(function(orderData) {
          // Successful capture! For dev/demo purposes:
              
              var transaction = orderData.purchase_units[0].payments.captures[0];
              

          // When ready to go live, remove the alert and show a success message within this page. For example:
          // var element = document.getElementById('paypal-button-container');
          // element.innerHTML = '';
          // element.innerHTML = '<h3>Thank you for your payment!</h3>';
          // Or go to another URL:  actions.redirect('thank_you.html');
             data = {
                'order_id': orderData.id,
            }
            $.ajax({
                
                method :"POST",
                url: "/order_by_paypal",
                data: data,
                success: function (responsec) {
                    alert("Success");
                    window.location.href = '/main_orders'
                    
                }
            });  
        });
      }
    }).render('#paypal-button-container');

  </script>

<script>
   $(document).ready(function(){

    $('#rzp-button1').click(function(){
      var address = $('input[name="address"]:checked').val();

      $.ajax({
        method : 'GET',
        url : '{% url "razorpay" %}',
        data : {
          address : address
        },
        success : function(response){
          console.log(response)

          var options = {
            "key": "rzp_test_xC4C7hryMBwbPF", // Enter the Key ID generated from the Dashboard
            "amount": response.total * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Ser Sha",
            "description": "Thank you for buying frim us",
            "image": "https://example.com/your_logo",
            // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response){
                alert(response.razorpay_payment_id);
                order_place();
            },
            "prefill": {
                "name": response.name,
                "email": response.email,
                "contact": response.phone
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();

        }
      })
      
    })

   })
</script>

<script>
$ (document).ready(function(){


  $('.payWithRazorpay').click(function(e){

      e.preventDefault();

      $.ajax({
          method: 'GET',
          url: "/pay_razorpay",
          success: function(response){
              console.log(response)
              var options = {
                  "key": "rzp_test_bjt6RpBlusedwC", // Enter the Key ID generated from the Dashboard
                  "amount": response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                  "currency": "INR",
                  "name": "GOGGLES Corporate",
                  "description": "Secured",
                  "image": "https://example.com/your_logo",
                  // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                  "handler": function (responseb){
                      
                      data = {
                              'order_id': responseb.razorpay_payment_id,
                      }
                      $.ajax({
                          
                          method :"POST",
                          url: "/order_by_razorpay",
                          data: data,
                          success: function (responsec) {
                              alert("Success");
                              window.location.href = '/main_orders'
                           
                          }
                      });
                  },
                  "prefill": {
                      "name": response.full_name,
                      "email": response.email,
                      "contact": response.phone_number,
                  },
                  "notes": {
                      "address": "Razorpay Corporate Office"
                  },
                  "theme": {
                      "color": "#3399cc"
                  }
              };
              var rzp1 = new Razorpay(options);
              rzp1.open();
          }
      })
  });
});

</script>

<script>
  var address = $('input[name="address"]:checked').val();
  $("#proceed").on("click", function (e) {
    order_place();
  });
  function order_place() {
    var payment = $('input[name="payment"]:checked').val();
    var address = $('input[name="address"]:checked').val();
    $.ajax({
      type: "POST",
      url: "{% url 'proceed' %}",
      data: {
        payment: payment,
        address: address,
        csrfmiddlewaretoken: "{{ csrf_token }}",
      },
      dataType: "json",
      success: function (response) {
        location = '{% url "home" %}';
      },
    });

  }

  $("input[type=radio][name=address]").change(function () {
    var id = "#" + $(this).val();
    var html = "<h3>SELECTED ADDRESS</h3>" + $(id).html();
    $(".selected").html(html);
    $(".selected input").remove();
  });

  $("input[type=radio][name=payment]").click(function () {
    var address = $('input[name="address"]:checked').val();
    var id = "div" + $(this).val();
    if (address != undefined) {
      if ($("#div_COD").hasClass("d-block")) {
        var element = document.getElementById("div_COD");
        element.classList.toggle("d-block");
        element.classList.toggle("d-none");
      }
      if ($("#div_PayPal").hasClass("d-block")) {
        var element = document.getElementById("div_PayPal");
        element.classList.toggle("d-block");
        element.classList.toggle("d-none");
      }
      if ($("#div_RazorPay").hasClass("d-block")) {
        var element = document.getElementById("div_RazorPay");
        element.classList.toggle("d-block");
        element.classList.toggle("d-none");
      }
      var element = document.getElementById(_id);
      element.classList.toggle("d-block");
      element.classList.toggle("d-none");
    } else {
      alert("please select address");
    }
  });
</script>

{% endblock %}
@never_cache
@login_required(login_url='signin')
def coupon_verify(request):
    customer = request.user
    input_code = request.GET.get('input_code')
    try :
        coupon = CouponDetail.objects.get(code=input_code)
    except :
        data = {'total_amount' : None,'percentage':None,}
        return JsonResponse(data)
    last = Order.objects.filter(cust = customer).order_by('-id')[0]
    if last.status == 'BuyNow' :
        order = Order.objects.get(cust = customer,status = 'BuyNow')
        items = OrderItem.objects.get(order = order)
    else :
        order= Order.objects.get(cust = customer,status = 'New')  
        items = order.orderitem_set.all()
    lessed_money = (order.get_cart_total * coupon.offer_percentage / 100)
    old_price = order.get_cart_total
    try :
        apply_coupon = CouponUsed.objects.filter(user = customer,coupon = coupon,used = False).first()
        print(apply_coupon)
    except:
        data = {'total_amount' : None,'percentage':None,}
        return JsonResponse(data)
    if apply_coupon is None :
        data = {'total_amount' : None,'percentage':'used',}
        return JsonResponse(data)

    apply_coupon.used = True
    apply_coupon.order = order
    apply_coupon.loss = int(lessed_money)
    apply_coupon.save()
    order.coupon_used = True
    CouponUsed.objects.get(user=customer,coupon=coupon).save()
    coupon.count = coupon.count + 1
    coupon.loss = coupon.loss +lessed_money
    coupon.save()
    order.save()
    data = {'total_amount' : order.get_cart_total,'percentage':coupon.offer_percentage,'old_price':old_price }
    return JsonResponse(data)