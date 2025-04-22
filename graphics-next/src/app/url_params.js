אתה יכול להשתמש ב־Next.js כדי לנהל פרמטרים של URL, אך זה יכול להיות מעט שונה מאשר בקוד המקורי שלך. Next.js משתמש ב־router כדי לנהל ניתוב, ואתה יכול להשתמש בו כדי לקבל את הפרמטרים של URL.

הנה דוגמה של קובץ שמשתמש ב־Next.js כדי לנהל פרמטרים של URL:

```jsx
import { useRouter } from 'next/router'

export default function Page() {
  const router = useRouter()

  function updateURLParameter(param, new_value) {
    let query = { ...router.query }

    if (new_value === 'None' || new_value === '') {
      delete query[param]
    } else {
      query[param] = new_value
    }

    router.push({
      pathname: router.pathname,
      query
    })
  }

  function hasURLParameter(key) {
    return router.query.hasOwnProperty(key)
  }

  // ...
}
```

בקוד המעודכן, אנחנו משתמשים ב־`useRouter` כדי לקבל את הנתב הנוכחי ואת הפרמטרים של ה־URL. אנחנו מעתיקים את הפרמטרים לאובייקט חדש כדי למנוע שינויים לא רצוניים בפרמטרים המקוריים, ואז אנחנו מעדכנים את הפרמטרים ומשתמשים ב־`router.push` כדי לעדכן את ה־URL.

שים לב שהקוד הזה יעבוד רק בתוך קומפוננטה של React, מכיוון שהוא משתמש ב-hook של React. אם אתה רוצה להשתמש בפונקציות אלה מחוץ לקומפוננטה, תצטרך להעביר את הנתב כפרמטר לפונקציות.