אתה יכול להמיר את הקובץ לקומפוננטת React שמתאימה ל־Next.js כך:

./components/BalanceProduct.js

התוכן:
-----
```jsx
import { useUser } from '../lib/hooks';
import { useRouter } from 'next/router';

const BalanceProduct = ({ balanceProduct }) => {
    const user = useUser();
    const router = useRouter();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Implement your form submission logic here
    }

    return (
        <form className="border-blue border-2 rounded-xl h-full p-5 flex gap-5 flex-col md:flex-row text-blue bg-white" method="post" onSubmit={handleSubmit}>
            <input className="" readOnly id="balance_product_id" name="balance_product_id" type="hidden" value={balanceProduct.id} />
            <div className="flex flex-col justify-between order-last md:order-first gap-2.5">
                {user && (
                    <button type="submit" className="mx-auto w-fit flex gap-4 items-center rounded-full font-bold text-lg py-2 px-5 hover:bg-gradient-2 border-2 border-blue" role="link">
                        <div className="rounded-full py-0.5 px-5 bg-blue text-white">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-6 h-6">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                            </svg>
                        </div>
                        Buy
                    </button>
                )}
                {balanceProduct.badge_text && (
                    <div className="mx-auto w-fit rounded-full font-bold text-base py-2 px-5 text-white bg-red-500">
                        <p>{balanceProduct.badge_text}</p>
                    </div>
                )}
            </div>
            <div className="flex flex-col gap-2.5 w-full">
                <p className="font-bold text-lg pb-2.5 border-b border-blue text-end">{balanceProduct.main_text}</p>
                <p className="font-bold text-lg pb-2.5 border-b border-blue text-end">{balanceProduct.help_text}</p>
                <p className="text-lg text-end">Balance replenishment <span className="text-orange font-bold">₪{balanceProduct.replenishment}</span></p>
            </div>
        </form>
    );
};

export default BalanceProduct;
```
-----
שים לב שאני מניח שיש לך hook בשם `useUser` שמחזיר את המשתמש הנוכחי, ואתה צריך לממש את הלוגיקה של שליחת הטופס בפונקציה `handleSubmit`.