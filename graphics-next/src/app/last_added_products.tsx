הקובץ ששלחת הוא קובץ תבנית Django, שהוא מערכת ניהול תוכן שנכתבה ב-Python. Next.js הוא סביבת פיתוח על בסיס Node.js שמאפשרת ליצור אתרים סטטיים ודינמיים ב-JavaScript.

אני אניח שהפונקציות `get_last_added_products` ו-`render_image_product` מגיעות ממודולים שאתה מייבא, ושהמשתנה `last_added_products` מגיע מה-props של הקומפוננטה.

הנה דוגמה לקובץ שמשתמש ב-React ו-Next.js:

```jsx
import { get_last_added_products, render_image_product } from '../your_module_path';

export default function LastAddedProducts({ last_added_products, reload_with_add_to_basket }) {
    const last_added_products_list = get_last_added_products(last_added_products.filters, last_added_products.display);

    return (
        <div id="last-added-products" className="mt-12">
            <style jsx>{`
                .pulse {
                    animation: my-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
                }
                @keyframes my-pulse {
                    0%, 100% {
                        opacity: 1;
                    }
                    50% {
                        opacity: .0;
                    }
                }
            `}</style>
            <div className="container">
                <h2 className="mx-2.5 text-blue text-end text-4xl sm:text-7xl leading-none font-bold flex items-center justify-end gap-2.5">
                    <span className="text-green border-2 border-blue rounded-full py-1 px-5 pulse">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                        </svg>
                    </span>
                    {last_added_products.title}
                </h2>
            </div>
            <div className="overflow-x-scroll">
                <div className="mt-12 flex gap-2.5 sm:gap-5 w-max pb-2.5 ml-auto" style={{ direction: 'rtl' }}>
                    {last_added_products_list.map(last_added_product =>
                        render_image_product(last_added_product, reload_with_add_to_basket)
                    )}
                </div>
            </div>
        </div>
    );
}
```

אני ממליץ לבדוק את הקוד שלך ולוודא שהוא עובד כמצופה, מאחר והמרת קוד ממערכת אחת למערכת אחרת יכולה להיות מורכבת ולדרוש התאמות.