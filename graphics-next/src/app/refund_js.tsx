ב-Next.js, אנחנו משתמשים ב-React ולכן נצטרך להמיר את הקוד הזה לקומפוננטת React. נשתמש בפונקציה fetch של JavaScript במקום $.ajax של jQuery. נשתמש גם בפונקציה useEffect של React במקום $(document).ready של jQuery. 

הנה הקוד המומר:

```jsx
import { useEffect, useRef } from 'react';

function RefundForm() {
  const formSuccessRef = useRef();
  const formErrorRef = useRef();
  const formRef = useRef();

  const refund = async () => {
    try {
      const response = await fetch('/salesman-order-refund', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') // נניח שיש לך פונקציה שמחזירה את הערך של עוגיה לפי שמה
        },
        body: JSON.stringify({ ref: object.ref }) // נניח ש-object.ref מגיע ממקום מסוים
      });

      if (!response.ok) {
        throw response;
      }

      const data = await response.json();
      formSuccessRef.current.querySelector('.msg').value = data.failed.length;
      formSuccessRef.current.submit();
    } catch (err) {
      err.json().then((data) => {
        if (data.non_field_errors) {
          alert(data.non_field_errors[0]);
        } else {
          formErrorRef.current.querySelector('.msg').value = data.detail;
          formErrorRef.current.submit();
        }
      });
    }
  };

  useEffect(() => {
    formRef.current.addEventListener('submit', (event) => {
      event.preventDefault();
      refund();
    });
  }, []);

  return (
    <>
      <form id="refund-form-success" ref={formSuccessRef}>
        {/* תוכן הטופס */}
      </form>
      <form id="refund-form-error" ref={formErrorRef}>
        {/* תוכן הטופס */}
      </form>
      <form id="refund-form" ref={formRef}>
        {/* תוכן הטופס */}
      </form>
    </>
  );
}

export default RefundForm;
```

אני מניח שיש לך פונקציה שמחזירה את הערך של עוגיה לפי שמה (getCookie בדוגמה) וש-object.ref מגיע ממקום מסוים. אם זה לא המקרה, תצטרך להתאים את הקוד לצרכים שלך.