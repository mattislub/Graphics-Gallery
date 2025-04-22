ב־Next.js, אנחנו משתמשים ב־React כדי ליצור קומפוננטות. ניתן להמיר את התבנית שלך לקומפוננטת React כך:

```jsx
import React from 'react';
import Image from 'next/image';
import { useRouter } from 'next/router';

export default function ImageProduct({
  product,
  isPaid,
  inBasket,
  inWishlist,
  availableBySubscription,
  getDownloadLink,
  getURLByPageName,
  reloadWithAddToBasket
}) {
  const router = useRouter();

  const productPrice = product.subscription_plans.length
    ? 'Free by subscription'
    : `${product.price} ₪`;

  const productIsPaid = isPaid;
  const productInBasket = inBasket || product.subscription_plans.length;
  const productInWishlist = inWishlist;

  const handleViewDetail = () => {
    // Logic to view product in detail
  };

  const handleWishlist = () => {
    // Logic to add/remove product from wishlist
  };

  const handleDownload = () => {
    window.open(getDownloadLink(product), '_blank');
    if (product.subscription_plans.length) {
      window.location.reload();
    }
  };

  const handleAddToBasket = () => {
    // Logic to add product to basket
    if (reloadWithAddToBasket) {
      window.location.reload();
    }
  };

  return (
    <div className="rounded-3xl relative w-fit mx-auto gap-2.5 my-2.5 group bg-gradient-2">
      <div className={`rounded-3xl h-40 sm:h-72 ${product.premium ? 'ring-4 ring-blue ring-opacity-60 p-1' : ''}`}>
        <Image src={product.preview_image_url} alt={product.code} className="h-full object-contain rounded-3xl bg-white min-w-36" />
      </div>
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-b from-blue hidden p-2.5 group-hover:block">
        <div className="flex flex-col items-center text-lg text-white text-center h-full">
          <a href={`${getURLByPageName('product')}${product.code}/`} className="w-full h-full overflow-hidden">
            <div className="text-xl">{product.name}</div>
            <div className="text-xl font-bold">{productPrice}</div>
          </a>
          <div className="flex gap-2 text-blue">
            <button className="rounded-full py-0.5 px-2 bg-white bg-opacity-70" onClick={handleViewDetail}>
              <span className="sr-only">View in detail</span>
              {/* SVG icon */}
            </button>
            <button className="rounded-full py-0.5 px-2 bg-white bg-opacity-70" onClick={handleWishlist}>
              <span className="sr-only">{productInWishlist ? 'Remove from wishlist' : 'Add to wishlist'}</span>
              {/* SVG icon */}
            </button>
            {isPaid || product.subscription_plans.length ? (
              <button className="rounded-full py-0.5 px-2 bg-orange text-white disabled:brightness-50" onClick={handleDownload}>
                <span className="sr-only">Download</span>
                {/* SVG icon */}
              </button>
            ) : (
              <button className="rounded-full py-0.5 px-2 bg-white bg-opacity-70 disabled:bg-gray-500" disabled={productInBasket} onClick={handleAddToBasket}>
                <span className="sr-only">Add to basket</span>
                {/* SVG icon */}
              </button>
            )}
          </div>
        </div>
      </div>
      {product.premium && (
        <div className="absolute left-8 top-7 font-bold bg-green rounded-full flex items-center gap-2 py-1 px-3 rotate-90 -translate-x-1/2 translate-y-full leading-none">
          <p>Premium</p>
          {/* SVG icon */}
        </div>
      )}
      {product.subscription_plans.length > 0 && (
        <div className="absolute right-8 top-11 font-bold bg-green rounded-full flex items-center gap-2 py-1 px-3 rotate-90 translate-x-1/2 translate-y-full leading-none">
          <p>Subscription</p>
          {/* SVG icon */}
        </div>
      )}
    </div>
  );
}
```

שים לב שהקוד הזה מניח שהנתונים מגיעים כתכונות לקומפוננטה. אתה תצטרך להתאים את הקוד לצורך שלך, למשל להוסיף את הלוגיקה לפונקציות המטפלות בלחיצות הכפתורים.