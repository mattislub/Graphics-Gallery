הקובץ ששלחת הוא קובץ Python שמשמש כקובץ סינון במערכת Django Admin. Next.js הוא סביבת פיתוח JavaScript שמבוססת על React, ולכן אין דרך ישירה להמיר את הקובץ ל-Next.js.

אם אתה מעוניין לבנות תכנות דומה ב-Next.js, תצטרך לבנות קומפוננטות React שמציגות את הנתונים ומאפשרות סינון שלהם. זה יכול להיראות כך:

```jsx
import { useState } from 'react';

// הנחה שיש לך פונקציה שמביאה את הנתונים מהשרת
import { getOrders } from './api/orders';

function OrdersPage() {
  const [statusFilter, setStatusFilter] = useState(null);
  const [isPaidFilter, setIsPaidFilter] = useState(null);

  const orders = getOrders();

  const filteredOrders = orders.filter(order => {
    if (statusFilter && order.status !== statusFilter) {
      return false;
    }

    if (isPaidFilter !== null && order.isPaid !== isPaidFilter) {
      return false;
    }

    return true;
  });

  return (
    <div>
      <select onChange={e => setStatusFilter(e.target.value)}>
        <option value="">All statuses</option>
        {/* הנחה שיש לך מערך של סטטוסים */}
        {statuses.map(status => (
          <option value={status}>{status}</option>
        ))}
      </select>

      <select onChange={e => setIsPaidFilter(e.target.value === '1')}>
        <option value="">All</option>
        <option value="1">Paid</option>
        <option value="0">Not paid</option>
      </select>

      {/* הצגת ההזמנות */}
      {filteredOrders.map(order => (
        <div key={order.id}>
          {/* הצגת פרטי ההזמנה */}
        </div>
      ))}
    </div>
  );
}

export default OrdersPage;
```

אני ממליץ להשתמש בספריה של ניהול מצבים (כמו Redux או MobX) או בפונקציות של React לניהול מצב (useState, useReducer) כדי לנהל את מצב הסינונים.