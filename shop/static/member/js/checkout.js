// promoData: { PID: { PromoCode: DisAmount, … }, … }
//var promoData = {{ promo_map_json|safe }};
var promoData = JSON.parse(JSON.parse(document.getElementById('promo_map_json').textContent));
const items = JSON.parse(document.getElementById('items').textContent);

function formatCardNumber(input) {
  let value = input.value.replace(/\D/g, '');
  let formattedValue = '';
  for (let i = 0; i < value.length; i++) {
    if (i > 0 && i % 4 === 0) {
      formattedValue += ' ';
    }
    formattedValue += value[i];
  }
  input.value = formattedValue.slice(0, 19);
}

function formatCardExp(input) {
    let value = input.value.replace(/\D/g, '');
    let formattedValue = '';
    for (let i = 0; i < value.length; i++) {
        if (i === 2) {
            formattedValue += '/';
        }
        formattedValue += value[i];
    }
    input.value = formattedValue.slice(0, 5);
}

function toggleCardFields(sel) {
  var cd = document.getElementById('card-details');
  var ch = document.getElementById('card_holder');
  var cn = document.getElementById('card_number');
  var ce = document.getElementById('card_expiry');
  var cc = document.getElementById('card_cvv');
  const creditCards = ['visa', 'mastercard'];
  if (creditCards.includes(sel.value.toLowerCase())) {
        cd.style.display = 'block';
        ch.setAttribute('required');
        cn.setAttribute('required', 'required');
        ce.setAttribute('required', 'required');
        cc.setAttribute('required', 'required');
  } else {
        cd.style.display = 'none';
        ch.removeAttribute('required');
        cn.removeAttribute('required');
        ce.removeAttribute('required');
        cc.removeAttribute('required');
  }
}

function togglePickupOptions(sel) {
  var div = document.getElementById('pickup-options');
  var pl = document.getElementById('pickup_location');
  if (sel.value === 'store_pickup') {
    div.style.display = 'block';
    pl.setAttribute('required', 'required');
  } else {
    div.style.display = 'none';
    pl.removeAttribute('required');
  }
}

function updateCheckoutTotals() {
  var rawTotal = 0, discountedTotal = 0;
  for (var i of items) {
      (function(){
        var pid   = `${ i.PID }`;
        var price = parseFloat(`${ i.Price }`);
        var qty   = parseInt(`${ i.Quantity }`);
        var code  = document.getElementById('promo-'+pid).value.trim();
        var disPer = 0, disAmt = 0;

        document.getElementById('promo-error-'+pid).textContent = '';

        if (code) {
          if (promoData[pid] && promoData[pid][code]) {
            disPer = promoData[pid][code];
            disAmt = disPer * qty;
          } else {
            document.getElementById('promo-error-'+pid).textContent =
              'Promo code not valid for this product';
          }
        }

        var sub     = price * qty;
        var subDisc = Math.max(sub - disAmt, 0);

        document.getElementById('discount-'+pid).textContent =
          'NT$' + disAmt.toFixed(2);
        document.getElementById('subtotal-'+pid).textContent =
          'NT$' + subDisc.toFixed(2);

        rawTotal       += sub;
        discountedTotal+= subDisc;
      })();
  }

  document.getElementById('total-raw').textContent =
    rawTotal.toFixed(2);
  document.getElementById('total-disc').textContent =
    discountedTotal.toFixed(2);
}

function validateForm() {
  var city   = document.getElementById('city').value;
  var dist   = document.getElementById('district').value;
  var street = document.getElementById('street').value.trim();
  if (!city || !dist || !street) {
    alert('Please complete the delivery address (City, District, Street & House No.).');
    return false;
  }
  var ship = document.getElementById('shipping').value;
  if (!ship) {
    alert('Please select a shipping method.');
    return false;
  }
  if (ship === 'store_pickup') {
    var loc = document.getElementById('pickup_location').value;
    if (!loc) {
      alert('Please select a pickup location.');
      return false;
    }
  }
  var pay = document.getElementById('pay_method').value;
  if (!pay) {
    alert('Please select a payment method.');
    return false;
  }
  return true;
}

window.onload = function() {
  for (var i of items) {
    document.getElementById('promo-' + `${i.PID}`)
            .addEventListener('input', updateCheckoutTotals);
  };
  document.getElementById('shipping')
          .addEventListener('change', function(e){ togglePickupOptions(e.target); });
  document.getElementById('pay_method')
          .addEventListener('change', function(e){ toggleCardFields(e.target); });

  const cardInput = document.querySelector('input[name="card_number"]');
  if (cardInput) {
    cardInput.addEventListener('input', function() { formatCardNumber(this); });
  }

  const expInput = document.querySelector('input[name="card_expiry"]');
  if (expInput) {
    expInput.addEventListener('input', function() { formatCardExp(this); });
  }

  updateCheckoutTotals();
  togglePickupOptions(document.getElementById('shipping'));
  toggleCardFields(document.getElementById('pay_method'));
}