ב-Next.js, אנחנו משתמשים ב-JSX במקום בתבניות Django. זה דורש כמה שינויים בקוד. כמו כן, אנחנו צריכים להשתמש בספריית React לטיפול במצבים ואירועים. נניח שאנחנו מקבלים את הנתונים שלנו כ-props מהקומפוננטה האב. הקוד שלך ייראה כך:

```jsx
import React, { useState, useEffect } from 'react';
import Image from 'next/image';

const MultiImagesBlock = ({ block }) => {
    const [page, setPage] = useState(1);

    useEffect(() => {
        const interval = setInterval(() => {
            if (page * 2 + 2 <= block.images.length) setPage(page + 1);
            else setPage(1);
        }, 5000);

        return () => clearInterval(interval);
    }, [page]);

    return (
        <div className="flex flex-wrap sm:flex-nowrap gap-5">
            <div className="flex gap-5 w-full min-h-20 basis-full sm:basis-1/2">
                {block.images.map((image, index) => (
                    <div key={index} className={`h-auto basis-1/2 rounded-2xl bg-cover bg-center ${index + 1 === page * 2 || index + 1 === page * 2 - 1 ? '' : 'hidden'}`}
                        style={{ backgroundImage: `url(${image.url})` }}></div>
                ))}
                <div className="flex flex-col justify-center gap-2.5">
                    {block.images.map((image, index) => {
                        if ((index + 1) % 2 === 0) {
                            const carouselPage = Math.ceil((index + 1) / 2);
                            return (
                                <div key={index} className={`bg-blue rounded-full w-4 h-4 cursor-pointer ${page === carouselPage ? '' : 'bg-opacity-10'}`}
                                    onClick={() => setPage(carouselPage)}></div>
                            );
                        }
                    })}
                </div>
            </div>
            <div className="flex gap-5 grow bg-blue bg-opacity-10 p-5 rounded-2xl justify-end">
                <div className="mt-auto">
                    <h3 className="font-bold text-2xl sm:text-4xl text-right">{block.title}</h3>
                    <div className="mt-3.5 text-end text-2xl sm:text-4xl">{block.text}</div>
                </div>
                <div className="flex flex-col gap-7">
                    <div className="p-2 rounded-2xl border-2 border-blue pulse" style={{ color: `#${block.icon.iconColor}` }}>
                        <Image src={block.icon.icon} className="w-11 h-11" />
                    </div>
                    <div className="mt-auto p-2 rounded-2xl border-2 border-blue text-center text-4xl md:text-7xl animate-bounce">
                        {block.images.length}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MultiImagesBlock;
```

אני מניח ש- `block` הוא אובייקט שמכיל את כל הנתונים שאתה צריך להציג את הקומפוננטה. אני משתמש בספריית `next/image` להצגת התמונות, אז אתה תצטרך להתקין אותה אם אתה עדיין לא משתמש בה.