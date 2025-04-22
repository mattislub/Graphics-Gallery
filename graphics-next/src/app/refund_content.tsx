ב־Next.js, אנחנו משתמשים ב־React ליצירת הממשק המשתמש. לכן, נצטרך להמיר את התבנית של Django לקומפוננטת React. נניח שכל הנתונים הנדרשים מסופקים כמאפיינים (props) לקומפוננטה.

```jsx
import { useState } from 'react';
import { format } from 'date-fns';

function RefundContent({ object, objectUrl }) {
  const [refundSuccess, setRefundSuccess] = useState(false);
  const [refundError, setRefundError] = useState(false);

  if (object.status === object.Status.REFUNDED) {
    return (
      <div>
        <p>Order is already marked as Refunded.</p>
        <form>
          <a href={objectUrl} className="button cancel-link button-secondary" style={{margin: 0}}>Go back</a>
        </form>
      </div>
    );
  }

  return (
    <div>
      <p>Are you sure you want to refund the Order <strong>{object}</strong>?</p>
      {object.payments.count && (
        <div>
          <p>All of the following payments will be refunded:</p>
          <ul>
            {object.payments.all.map(payment => (
              <li key={payment.id}>
                <strong>{payment}</strong>
                {payment.payment_method && ` using ${payment.payment_method_display}`}
                on <i>{format(new Date(payment.date_created), 'yyyy-MM-dd')}</i>.
              </li>
            ))}
          </ul>
        </div>
      )}
      <br />
      <form id="refund-form">
        <input type="submit" value="Yes, I’m sure" className="button serious" />
        <a href={objectUrl} className="button cancel-link button-secondary">No, take me back</a>
      </form>
      <form id="refund-form-success" method="post">
        <input className="msg" type="hidden" name="_refund-success" value={refundSuccess} />
      </form>
      <form id="refund-form-error" method="post">
        <input className="msg" type="hidden" name="_refund-error" value={refundError} />
      </form>
    </div>
  );
}

export default RefundContent;
```

שים לב שאנחנו משתמשים בספריית date-fns לפורמט התאריך. כמו כן, הקוד מניח שהמאפיינים `object` ו-`objectUrl` מסופקים לקומפוננטה.