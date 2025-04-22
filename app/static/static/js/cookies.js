function setCookieObject(name, value, options = {}) {
    options = {
        path: '/',
        ...options
    };
  
    if (!options.expires) {
      options.expires = new Date('9999-12-31T23:59:59Z');
    }
  
    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }
  
    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(JSON.stringify(value));
  
    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }
  
    document.cookie = updatedCookie;
  }
  
function getCookieObject(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? JSON.parse(decodeURIComponent(matches[1])) : undefined;
}
  
function deleteCookie(name) {
    setCookieObject(name, "", {
        'max-age': -1
    });
}
  