ב-Next.js, אנחנו משתמשים ב-JSX במקום תבניות Django. כמו כן, אנחנו משתמשים בקומפוננטות React במקום בלוקים Django. כאן הוא הקובץ שהומר ל-Next.js:

./components/ComparingBlock.js

התוכן:
-----
```jsx
import Image from 'next/image';
import { useEffect } from 'react';

function ComparingBlock({ block }) {
    const { title, text, icon, image_1, image_2 } = block;

    useEffect(() => {
        // יש להתקין את jQuery והספרייה twentytwenty באמצעות npm או yarn
        // ולאחר מכן לייבא אותם כאן
        const $ = require('jquery');
        require('jquery.event.move');
        require('jquery.twentytwenty');

        $(document).ready(function() {
            $("#comparing-container").twentytwenty({'no_overlay': true});
        });
    }, []);

    return (
        <div className="flex flex-wrap md:flex-nowrap gap-5">
            <div className="flex gap-5 bg-blue grow bg-opacity-10 p-5 rounded-2xl justify-end">
                <div className="mt-auto">
                    <h3 className="font-bold text-2xl sm:text-4xl text-right">{title}</h3>
                    <div className="mt-3.5 text-end text-2xl sm:text-4xl">{text}</div>
                </div>
                <div className="flex flex-col gap-7">
                    <div className="p-2 rounded-2xl border-2 border-blue pulse" style={{color: `#${icon.icon_color}`}}>
                        {/* יש להמיר את התג svg_icon לקומפוננטת React */}
                    </div>
                    <div className="mt-auto p-2 rounded-2xl border-2 border-blue text-center text-4xl md:text-7xl animate-bounce">
                        {/* יש להחליף את forloop.counter במשתנה מתאים */}
                    </div>
                </div>
            </div>
            <div className="m-auto basis-1/3 lg:basis-1/4">
                <div id="comparing-container" className="rounded-2xl max-h-fit">
                    <Image className="h-auto" src={image_1.url} alt="comparing-image-1" />
                    <Image className="h-auto" src={image_2.url} alt="comparing-image-2" />
                </div>
            </div>
        </div>
    );
}

export default ComparingBlock;
```
-----
אני מניח שהקובץ CSS twentytwenty.css והספריות jQuery ו-twentytwenty מותקנות באמצעות npm או yarn. אם לא, תצטרך להתקין אותם ולייבא אותם בקובץ ה-JS שלך.