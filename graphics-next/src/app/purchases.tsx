ב-Next.js, נשתמש ב-React ליצירת הקומפוננטות שלנו. נצטרך להמיר את התבנית שלנו לקומפוננטת React. נניח שכל הפונקציות והנתונים שאנחנו משתמשים בהם בתבנית זמינים כ-props.

```jsx
import React from 'react';

function PurchasesPage({ userPurchasedProducts, changePageUrl, translate }) {
  return (
    <div className="mt-12 grow container">
        <div className="mx-2.5">
            {/* Include user panel block component */}
        </div>
        <div id="wishlist-list-container" className="mt-12 flex flex-wrap gap-2.5 sm:gap-5" style={{direction: 'rtl'}}>
            {userPurchasedProducts.map(product => (
                // Render image product component
            ))}
        </div>
        <div className="flex mt-12 flex-wrap gap-5 justify-end">
            <div className="flex flex-wrap mx-auto gap-5 justify-center">
                {userPurchasedProducts.hasNext ? (
                    <a href={changePageUrl(userPurchasedProducts.nextPageNumber)} className="w-52 flex gap-4 items-center justify-between rounded-full font-bold text-lg py-2 px-5 hover:bg-gradient-2 border-2 border-blue disabled:border-slate-500">
                        <div className="rounded-full py-0.5 px-5 bg-blue text-white">
                            {/* SVG */}
                        </div>
                        <p>{translate('Next')}</p>
                    </a>
                ) : (
                    <div className="w-52 flex gap-4 items-center justify-between rounded-full font-bold text-lg py-2 px-5 border-2 border-slate-400 text-slate-400">
                        <div className="rounded-full py-0.5 px-5 bg-slate-500 text-white">
                            {/* SVG */}
                        </div>
                        <p>{translate('Next')}</p>
                    </div>
                )}
                
                {userPurchasedProducts.hasPrevious ? (
                    <a href={changePageUrl(userPurchasedProducts.previousPageNumber)} className="w-52 flex gap-4 items-center justify-between rounded-full font-bold text-lg py-2 px-5 hover:bg-gradient-2 border-2 border-blue">
                        <p>{translate('Previous')}</p>
                        <div className="rounded-full py-0.5 px-5 bg-blue text-white">
                            {/* SVG */}
                        </div>
                    </a>
                ) : (
                    <div className="w-52 flex gap-4 items-center justify-between rounded-full font-bold text-lg py-2 px-5 border-2 border-slate-400 text-slate-400">
                        <p>{translate('Previous')}</p>
                        <div className="rounded-full py-0.5 px-5 bg-slate-500 text-white">
                            {/* SVG */}
                        </div>
                    </div>
                )}
            </div>
            <div className="flex text-xl items-center">
                <p>{translate('from')} {userPurchasedProducts.paginator.numPages}</p>
                <div className=" ml-10">
                    {/* SVG */}
                </div>                    
                <div className="rounded-full border-2 px-4 border-blue font-bold my-auto">
                    <p>{userPurchasedProducts.number}</p>
                </div>
                {/* SVG */}
            </div>
        </div>
    </div>
  );
}

export default PurchasesPage;
```

אני לא המרתי את הקוד SVG והקומפוננטות שאנחנו משתמשים בהם כי אני לא יודע איך הם נראים. אתה יכול להמיר אותם לקומפוננטות React ולהשתמש בהם בקוד שלך.