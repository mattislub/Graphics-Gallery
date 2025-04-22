ב-Next.js, אנחנו משתמשים ב-JavaScript וב-React במקום בתבניות Django. לכן, נצטרך להמיר את הקוד שלך לקומפוננטת React. הנה דוגמה לכך:

```jsx
import { useState } from 'react';

function BasketPreviewBlock({ basket, reloadWithRemoveFromBasket }) {
  return (
    <div className="flex flex-col max-h-96 overflow-y-auto z-50">
      {basket.items.map((basketItem) => {
        const [show, setShow] = useState(true);

        const handleClick = () => {
          // TODO: Implement basket.remove
          // basket.remove(basketItem.ref, basketItem.product.code);

          if (reloadWithRemoveFromBasket) {
            window.location.reload();
          } else {
            // TODO: Implement dispatch
            // dispatch(`basket_${basketItem.product_id}`, false);
            setShow(false);
          }
        };

        return show ? (
          <div key={basketItem.ref} className="flex gap-2.5 sm:gap-5 border-t last:border-b first:border-t-0 border-blue py-2.5">
            <div className="flex items-start gap-5">
              <div className="flex flex-col h-full items-center">
                {basketItem.product.premium && (
                  <div className="font-bold bg-green rounded-full flex items-center gap-2 py-1 px-3 eading-none">
                    {/* TODO: Replace with actual SVG */}
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                    </svg>
                  </div>
                )}
                <button className="mt-auto" onClick={handleClick}>
                  <span className="sr-only">Remove from basket</span>
                  {/* TODO: Replace with actual SVG */}
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6 stroke-gray-400 hover:stroke-gray-700">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="ml-auto">
              <h3 className="leading-tight font-normal tracking-widest text-end">{basketItem.product.name}</h3>
              <p className="text-xs leading-tight text-end mt-2.5">{basketItem.product.code}</p>
              <p className="my-auto text-base font-bold text-end text-orange">{basketItem.product.price} ₪</p>
            </div>
            <img className="object-fit h-16 self-center rounded-xl" alt={basketItem.product.name} src={basketItem.product.preview_image_url} />
          </div>
        ) : null;
      })}
    </div>
  );
}

export default BasketPreviewBlock;
```

שים לב שאני מניח שאתה מספק את האובייקט `basket` כ-prop לקומפוננטה. כמו כן, אני מניח שאתה מספק prop בשם `reloadWithRemoveFromBasket` שמציין אם צריך לרענן את הדף בעת הסרת פריט מהסל. אני גם מניח שיש לך מנגנון לניהול מצב שמאפשר לך להסיר פריטים מהסל ולשלוח אירועים.