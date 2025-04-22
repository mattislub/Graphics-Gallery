ב־Next.js, ניתן ליצור קומפוננטות React שמייצגות דפים. ניתן להמיר את הקובץ הנ"ל לקומפוננטה של Next.js כך:

צור קובץ בשם 500.js בתוך התיקייה pages:

./pages/500.js

התוכן:
-----
```jsx
import Head from 'next/head'

export default function Custom500() {
    return (
        <div>
            <Head>
                <title>Internal server error</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <meta charset="utf-8" />
            </Head>
            <h1>Internal server error</h1>
            <h2>Sorry, there seems to be an error. Please try again soon.</h2>
        </div>
    )
}
```
-----

בקוד הנ"ל, אנחנו מייבאים את הקומפוננטה Head מהספרייה 'next/head' כדי להוסיף תגיות לתוך הכותרת של הדף. אז אנחנו מייצרים קומפוננטה שמציגה את ההודעה של שגיאה 500.