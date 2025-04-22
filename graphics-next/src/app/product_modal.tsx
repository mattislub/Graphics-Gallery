ב־Next.js, אנחנו משתמשים ב־React כדי ליצור קומפוננטות. נכתוב את הקומפוננטה שלנו בצורה שתתאים ל־React:

```jsx
import React, { useState, useEffect } from 'react';

const ProductModal = () => {
  const [open, setOpen] = useState(false);
  const [productIndex, setProductIndex] = useState(-1);
  const [productList, setProductList] = useState(null);
  const [product, setProduct] = useState({
    id: '',
    code: '',
    type: '',
    name: '',
    price: '',
    buttons: '',
    isPaid: '',
    inBasket: '',
    inWishlist: '',
    displayUrl: '',
  });

  const openModal = () => {
    // Your open modal logic here
  };

  const closeModal = () => {
    // Your close modal logic here
  };

  const updateProductByIndex = () => {
    // Your update product by index logic here
  };

  useEffect(() => {
    updateProductByIndex();
  }, [productIndex]);

  return (
    <div className={`fixed inset-0 z-[99999] overflow-auto bg-white flex flex-col ${open ? 'block' : 'hidden'}`} role="dialog">
      <button className="fixed top-28 left-6 z-[99] text-blue hover:opacity-60" onClick={closeModal}>Close</button>
      {/* Rest of your JSX here */}
    </div>
  );
};

export default ProductModal;
```

אני מניח שיש לך קוד עסקי מסוים שאתה רוצה להוסיף לפונקציות `openModal`, `closeModal` ו־`updateProductByIndex`. אתה יכול להוסיף את הקוד שלך לפונקציות האלה.

בנוסף, אני מניח שיש לך דרך לקבל את `productList` מהסביבה שלך. אתה יכול להשתמש ב־`setProductList` כדי לעדכן את המצב של `productList`.

לבסוף, אני מניח שיש לך דרך לקבל את האירועים של המקשים שאתה מאזין להם. אתה יכול להוסיף את הקוד שלך לקומפוננטה כדי להאזין לאירועים אלה.