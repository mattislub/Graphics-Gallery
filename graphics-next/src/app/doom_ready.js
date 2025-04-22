ב-Next.js, ניתן להשתמש ב-React Hooks כדי להגיב לאירועים של ה-DOM. לדוגמה, ניתן להשתמש ב-Hook useEffect כדי להגיב לאירוע "DOMContentLoaded". הנה דרך אחת להמיר את הקוד הנתון ל-Next.js:

```jsx
import { useEffect } from 'react';

export default function MyComponent() {
  useEffect(() => {
    function domReady(event) {
      // הפונקציה שאתה רוצה להפעיל כאשר ה-DOM מוכן
    }

    if (document.readyState === "loading") {  // Loading has not finished yet
      document.addEventListener("DOMContentLoaded", domReady);
    } else {  // `DOMContentLoaded` has already fired
      domReady();
    }

    // נקה את האירוע כאשר הקומפוננטה מתנתקת
    return () => {
      document.removeEventListener("DOMContentLoaded", domReady);
    };
  }, []);  // הפעל רק פעם אחת, כאשר הקומפוננטה מוכנה

  // תוכן הקומפוננטה שלך
  return <div>...</div>;
}
```

בקוד הנ"ל, אנחנו משתמשים ב-Hook useEffect כדי להפעיל קוד כאשר הקומפוננטה מוכנה לשימוש, וכאשר היא מתנתקת. אנחנו מגדירים את הפונקציה domReady שאנחנו רוצים להפעיל כאשר ה-DOM מוכן, ואז אנחנו מרשמים אותה כמאזין לאירוע "DOMContentLoaded". אם האירוע כבר התרחש, אנחנו מפעילים את הפונקציה מיד. לבסוף, אנחנו מנקים את האירוע כאשר הקומפוננטה מתנתקת.