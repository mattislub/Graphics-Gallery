קוד ה-HTML שלך משתמש בתבנית Django, ואנחנו צריכים להמיר אותו לקומפוננטת React שתתאים ל-Next.js. נכתוב קומפוננטת React בסיסית שתכיל את התוכן שלך. נכתוב גם קוד פשוט שישתמש ב-React Hooks כדי להחזיק את מצב המשתמש (אם הוא מחובר או לא). נכתוב גם קוד פשוט שישתמש ב-React Hooks כדי להחזיק את מצב המשתמש (אם הוא מחובר או לא).

אני מניח שיש לך קובץ קומפוננטה ב-Next.js שנקרא `RootPage.js`. הקוד הבא הוא דוגמה לקובץ זה:

```jsx
import React, { useState } from 'react';

const RootPage = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  return (
    <div className="flex flex-col justify-between min-h-screen text-blue">
      <div className="mx-6 mt-6 z-50">
        <header id="header" className="flex border border-blue p-3 rounded-full gap-4 bg-white">
          <nav id="nav" className="flex items-center grow">
            <div className="hidden items-center md:flex justify-between w-full">
              <div className="flex items-center gap-2 lg:gap-4">
                {isAuthenticated ? (
                  <>
                    <a href="/profile" className="rounded-full font-normal text-base border-2 border-blue bg-blue text-white py-0.5 px-5 hover:bg-gradient-2">
                      Account
                    </a>
                    <p className="block font-normal text-base leading-8">Balance: {user.balance}</p>
                  </>
                ) : (
                  <a href="/login" className="rounded-full bg-blue text-white py-0.5 px-5 hover:opacity-60">
                    Log in
                  </a>
                )}
                {/* ...rest of your code... */}
              </div>
            </div>
          </nav>
        </header>
      </div>
      {/* ...rest of your code... */}
    </div>
  );
};

export default RootPage;
```

שים לב שהקוד הזה הוא רק דוגמה ואתה תצטרך להתאים אותו לצרכים שלך. לדוגמה, תצטרך להחליף את הקישורים הקשיחים בקוד שלך בקישורים דינמיים שמשתנים בהתאם למצב של האפליקציה. כמו כן, תצטרך להוסיף קוד לטיפול באירועים כמו לחיצה על כפתור ההתחברות.