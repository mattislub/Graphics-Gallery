ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) וב-React ליצירת הקומפוננטות שלנו. ניתן להשתמש ב-Hooks כדי לטעון נתונים מהשרת. במקרה שלנו, אנחנו צריכים לטעון את השאילתות הפופולריות. נניח שיש לנו API שמחזיר את הנתונים האלה.

הנה דוגמה לקובץ שממומש ב-Next.js:

```jsx
import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function PopularQueries() {
    const [popularQueries, setPopularQueries] = useState({ current_option: ['tags', ''], title: '', display: false, new_tab: false, list: [] });

    useEffect(() => {
        // Replace with your API call
        fetch('/api/popular_queries')
            .then(response => response.json())
            .then(data => setPopularQueries(data));
    }, []);

    return (
        <div id="popular-queries" className="mt-12 container">
            <div className="mx-2.5">
                <h2 className="text-blue text-end text-4xl sm:text-7xl leading-none font-bold">
                    <span className="text-light_blue">
                        {popularQueries.current_option[1]}
                    </span>
                    {popularQueries.title}
                </h2>
                <div className="mt-12 flex flex-wrap gap-2.5 sm:gap-5" style={{ direction: 'rtl' }}>
                    {popularQueries.list.map((popularQuery, index) => (
                        popularQueries.current_option[0] === 'tags' ?
                            <Link href={`/images?search=${popularQuery.name}`} key={index}>
                                <a target={popularQueries.new_tab ? "_blank" : "_self"} className="border border-blue text-blue px-2 py-1 rounded-full hover:bg-blue hover:bg-opacity-30 hover:text-white hover:border-transparent">{popularQuery.name}</a>
                            </Link>
                            :
                            <Link href={`/images?image-category=${popularQuery.slug}`} key={index}>
                                <a target={popularQueries.new_tab ? "_blank" : "_self"} className="border border-blue text-blue px-2 py-1 rounded-full hover:bg-blue hover:bg-opacity-30 hover:text-white hover:border-transparent">{popularQuery.name}</a>
                            </Link>
                    ))}
                </div>
            </div>
        </div>
    );
}
```

הקוד מניח שיש לך API שמחזיר את הנתונים הנדרשים. אתה תצטרך להחליף את ה-URL של ה-API בקריאה ל-fetch.