ב-Next.js, אנחנו יכולים להשתמש בקומפוננטות React כדי ליצור את הפונקציונליות שלנו. ניתן להמיר את הפונקציות שלך לקומפוננטות React, כך:

```jsx
import { useState, useEffect } from 'react';

// המרת הפונקציה show_hide_password לקומפוננטת React
export function ShowHidePassword({ element, inputId }) {
  const [inputType, setInputType] = useState('password');

  const togglePasswordVisibility = () => {
    setInputType(inputType === 'password' ? 'text' : 'password');
  };

  return (
    <div onClick={togglePasswordVisibility}>
      {inputType === 'password' ? 'Show' : 'Hide'}
    </div>
  );
}

// המרת הפונקציה enable_profile_edit לקומפוננטת React
export function EnableProfileEdit({ children }) {
  const [isEditable, setIsEditable] = useState(false);

  const toggleEdit = () => {
    setIsEditable(!isEditable);
  };

  return (
    <div onClick={toggleEdit}>
      {isEditable ? 'Save' : 'Edit'}
      {React.cloneElement(children, { disabled: !isEditable })}
    </div>
  );
}

// המרת הפונקציה load_from_cookies לקומפוננטת React
export function LoadFromCookies() {
  useEffect(() => {
    const wishlist = getCookieObject('wishlist');
    const basket = getCookieObject('basket');

    if (wishlist || basket) {
      if (wishlist) {
        wishlist.forEach((code) => {
          fetch(`/user/add-to-wishlist/${code}/`, {
            method: 'GET',
          }).then((response) => response.text());
        });
      }

      if (basket) {
        basket.forEach((element) => {
          add_to_basket(element[0], element[1], element[2]);
        });
      }

      deleteCookie('wishlist');
      deleteCookie('basket');

      document.location.reload();
    }
  }, []);

  return null;
}
```

אני מניח שהפונקציות `getCookieObject`, `add_to_basket` ו-`deleteCookie` מוגדרות במקום אחר בקוד שלך. אם זה לא המקרה, תצטרך להגדיר אותן.