function updateURLParameter(param, new_value) {
    let url = new URL(window.location.href);
    let params = new URLSearchParams(url.search);
  
    if (new_value === 'None' || new_value === '') {
      params.delete(param)
    } else {
      if (params.has(param)) {
        params.set(param, new_value);
      } else {
        params.append(param, new_value);
      }
    }
  
      url.search = params.toString();
      window.location = url.toString();
  }
  
function hasURLParameter(key) {
    const urlParams = new URLSearchParams(window.location.search);

    return urlParams.has(key);
}