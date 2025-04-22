ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) ו-React במקום Django templates. הקובץ המומר יראה כך:

./app/salesman_admin/components/SalesmanAdminWagtailEdit.js

התוכן:
-----
```jsx
import { useState } from 'react';
import { useTranslation } from 'next-i18next';

function SalesmanAdminWagtailEdit({ view }) {
  const { t } = useTranslation('salesman');
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = () => {
    setIsSaving(true);
    // TODO: Implement save logic here.
  };

  return (
    <>
      <div className="salesman-order-form">
        {/* TODO: Render form here. */}
      </div>

      <footer className="footer">
        <ul style={{ display: 'flex' }}>
          <li className="footer__container">
            <div className="dropdown dropup dropdown-button match-width">
              <button
                type="submit"
                className="button action-save button-longrunning"
                onClick={handleSave}
              >
                {/* TODO: Replace with actual spinner icon. */}
                <em>{isSaving ? t('Saving…') : t('Save')}</em>
              </button>
            </div>
          </li>

          {view.refund_url && (
            <li className="preview footer__container">
              <a href={view.refund_url} className="button" style={{ minHeight: '39px' }}>
                {t('Refund order')}
              </a>
            </li>
          )}
        </ul>
      </footer>
    </>
  );
}

export default SalesmanAdminWagtailEdit;
```
-----

אני מניח שיש לך קומפוננטת טופס שאתה רוצה להציג בתוך ה-div `salesman-order-form`. אתה יכול להוסיף אותו במקום ההערה `TODO: Render form here.`.

בנוסף, אני מניח שיש לך אייקון של spinner שאתה רוצה להציג במקום ההערה `TODO: Replace with actual spinner icon.`.

אני משתמש ב-`useState` כדי לשמור על מצב של הכפתור שמר. אתה תצטרך להוסיף את הלוגיקה של שמירת הטופס בתוך הפונקציה `handleSave`.

אני משתמש ב-`useTranslation` מ-`next-i18next` כדי לתמוך בתרגום. אתה תצטרך להוסיף את המילים שאתה רוצה לתרגם לקובץ התרגום שלך.