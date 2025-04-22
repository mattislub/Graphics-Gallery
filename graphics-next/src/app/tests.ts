ב-Next.js, אין תמיכה ישירה בטסטים כמו ב-Python. על מנת לבצע טסטים, אנו יכולים להשתמש בספריות כמו Jest ו-React Testing Library. קובץ הטסטים יהיה כמו הבא:

./app/shop/tests.js

התוכן:
-----
import { render, screen } from '@testing-library/react';
import Shop from './shop';

test('renders learn react link', () => {
  render(<Shop />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
-----

אני מניח שיש לך קומפוננטה בשם Shop שאתה רוצה לבדוק. הקוד מעלה מריץ טסט שבודק אם הטקסט "learn react" מופיע בקומפוננטה. אתה יכול להתאים את הטסט לצרכים שלך.

אל תשכח להתקין את הספריות הנדרשות על ידי הרצת הפקודות הבאות בשורת הפקודה:

npm install --save-dev jest @testing-library/react @testing-library/jest-dom

ולהוסיף את הסקריפט הבא לקובץ package.json שלך:

"scripts": {
  "test": "jest"
}