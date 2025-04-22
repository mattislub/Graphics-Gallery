המרת קוד Python ל-JavaScript ו-Next.js יכולה להיות מורכבת, מאחר שהשפות משתמשות בפרדיגמות שונות וישנם רבים ספריות ופריימוורקים שונים בשפה. עם זאת, הנה דוגמה של איך יכול להיראות קובץ Next.js שמבצע פונקציונליות דומה:

```jsx
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import axios from 'axios';

const OrderAdmin = () => {
  const router = useRouter();
  const [orders, setOrders] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    axios.get('/api/orders')
      .then(res => setOrders(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleSearch = e => {
    setSearch(e.target.value);
  };

  const filteredOrders = orders.filter(order =>
    order.ref.includes(search) ||
    order.email.includes(search) ||
    order.token.includes(search)
  );

  return (
    <div>
      <input type="text" value={search} onChange={handleSearch} placeholder="Search..." />
      <ul>
        {filteredOrders.map(order => (
          <li key={order.id}>
            <h2>{order.__str__}</h2>
            <p>{order.email}</p>
            <p>{order.status_display}</p>
            <p>{order.total_display}</p>
            <p>{order.is_paid_display}</p>
            <p>{order.date_created}</p>
            <button onClick={() => router.push(`/orders/${order.id}`)}>Edit</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OrderAdmin;
```

שים לב שהקוד הזה מניח שיש לך API שמחזיר את ההזמנות שלך בנתיב '/api/orders', ושיש לך דף עריכה בנתיב '/orders/[id]'. זה גם משתמש בספריית axios לביצוע בקשות HTTP, אז תוודא שהתקנת אותה באמצעות `npm install axios` או `yarn add axios`.