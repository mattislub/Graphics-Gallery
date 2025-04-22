הקובץ שלך משתמש בתבניות Django, אך Next.js משתמש ב-JavaScript ו-React. כאן יש דוגמה של איך יכול להיראות הקובץ שלך ב-Next.js:

./components/SimilarProducts.js

```jsx
import { useEffect, useState } from 'react';
import ImageProduct from './ImageProduct';

const SimilarProducts = ({ similarProducts, reloadWithAddToBasket }) => {
    const [similarProductsList, setSimilarProductsList] = useState([]);

    useEffect(() => {
        // כאן אתה צריך להחליף את הפונקציה get_similar_products שלך
        // עם קריאת API או פונקציה אחרת שתחזיר את המוצרים הדומים
        getSimilarProducts(similarProducts.filters, similarProducts.display)
            .then(products => setSimilarProductsList(products));
    }, [similarProducts]);

    return (
        <div id="similar-products" className="mt-12 container">
            <div className="mx-2.5">
                <h2 className="text-blue text-end text-4xl sm:text-7xl leading-none font-bold flex items-center justify-end gap-2.5">
                    <span className="text-orange border-2 border-blue rounded-full py-2 px-3.5 pulse">
                        <svg xmlns="http://www.w3.org/2000/svg" width="72" height="17" viewBox="0 0 72 17" fill="none">
                            <path d="M0.399789 9.41385L0.401009 9.41514L7.5218 16.5016C8.05526 17.0325 8.91811 17.0305 9.44912 16.497C9.98005 15.9635 9.97801 15.1007 9.44455 14.5697L4.66364 9.81199L69.999 9.81199C70.7517 9.81199 71.3618 9.20188 71.3618 8.44921C71.3618 7.69655 70.7517 7.08644 69.999 7.08644L4.66371 7.08643L9.44449 2.32869C9.97794 1.79775 9.97999 0.934911 9.44905 0.401451C8.91804 -0.132145 8.05513 -0.133983 7.52174 0.396818L0.400941 7.48327L0.39972 7.48456C-0.13401 8.01727 -0.132308 8.88291 0.399789 9.41385Z" fill="currentColor"/>
                        </svg>
                    </span>
                    {similarProducts.title}
                </h2>
                <div className="mt-12 flex flex-wrap gap-2.5 sm:gap-5" style={{ direction: 'rtl' }}>
                    {similarProductsList.map(product => (
                        <ImageProduct key={product.id} product={product} reloadWithAddToBasket={reloadWithAddToBasket} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default SimilarProducts;
```

אני מניח שיש לך קומפוננטה שמציגה מוצר בתמונה (`ImageProduct`) ופונקציה שמחזירה מוצרים דומים (`getSimilarProducts`). אתה תצטרך להתאים את הקוד לפי הקוד שלך.