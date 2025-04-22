ב־Next.js, אנחנו משתמשים בקומפוננטות React במקום תבניות Django. ניתן להמיר את הקובץ שלך לקומפוננטה React באופן הבא:

```jsx
import { useEffect, useState } from 'react';
import Head from 'next/head';
import Script from 'next/script';

export default function LoadProductsResult() {
    const [key, setKey] = useState('');
    const [savingInfo, setSavingInfo] = useState('No information');

    useEffect(() => {
        const checkStatus = () => {
            fetch('/check-load-products/' + '?key=' + key, {method: 'GET'})
            .then(response => response.json())
            .then((response) => {
                if (response['status'] === 'error') {
                    setSavingInfo('ERROR');
                }
                else if (response['status'] === 'progress') {
                    setSavingInfo(response['current'] + ' / ' + response['total']);
                    setTimeout(checkStatus, 1000);
                }
                else if (response['status'] === 'success') {
                    setSavingInfo('all');
                }
            });
        };

        setTimeout(checkStatus, 500);
    }, [key]);

    return (
        <>
            <Head>
                <title>Multiple Product Loading</title>
            </Head>

            <Script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.3/dist/cdn.min.js" />

            <div className="nice-padding">
                <h2>Images saved: {savingInfo}</h2>
                <a className="page404__button button" href="/admin/">Go to Wagtail admin</a>
            </div>
        </>
    );
}
```

שים לב שהקוד הזה מניח שיש לך קומפוננטה של כותרת עם הסמל והכותרת שאתה מעביר לה. אם אין לך קומפוננטה כזו, תצטרך להוסיף אותה לקוד שלך.