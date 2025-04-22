function show_hide_password(element, input_id) {
  input = document.getElementById(input_id);

  if (input.getAttribute('type') === 'password') {
    input.setAttribute('type', 'text');
    element.querySelector('#show').classList.add('hidden');
    element.querySelector('#hide').classList.remove('hidden');
  }
  else {
    input.setAttribute('type', 'password');
    element.querySelector('#show').classList.remove('hidden');
    element.querySelector('#hide').classList.add('hidden');
  }
}

function enable_profile_edit() {
  document.querySelectorAll('#edit').forEach(function(element) {
    element.classList.add('hidden');
  });

  document.querySelectorAll('#save').forEach(function(element) {
    element.classList.remove('hidden');
  });

  document.querySelectorAll('input').forEach(function(element) {
    element.disabled=false;
    if (element.parentElement.parentElement.classList.contains('hidden')) element.parentElement.parentElement.classList.remove('hidden');
  });
}

function load_from_cookies() {
  let wishlist = getCookieObject('wishlist');
  let basket = getCookieObject('basket');
  if (wishlist !== undefined || basket !== undefined) {
    if (wishlist !== undefined)
      wishlist.forEach(function(code, index) {
        fetch('/user/add-to-wishlist/' + code + '/', {
          method: 'GET',
        }).then(response => response.text())
        .then(response => {});
    });

    if (basket !== undefined)
      basket.forEach(function(element, index) {
        add_to_basket(element[0], element[1], element[2]);
    });

    deleteCookie('wishlist');
    deleteCookie('basket');

    document.location.reload();
  }
}
