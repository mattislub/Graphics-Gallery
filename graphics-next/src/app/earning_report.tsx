ב־Next.js, אנחנו משתמשים ב־React ליצירת קומפוננטות UI. לכן, נצטרך להמיר את התבנית שלנו לקומפוננטת React. נניח שכל הנתונים הנדרשים מגיעים כמאפיינים (props) לקומפוננטה.

```jsx
import React from 'react';

const EarningReport = ({ form, total_amount, object_list }) => (
  <div>
    <form action="" method="get">
      <div>
        <label htmlFor="date_from">{form.fields.date_from.label}</label>
        <input type="date" name="date_from" id="date_from" value={form.date_from.value} />
      </div>
      <div>
        <label htmlFor="date_to">{form.fields.date_to.label}</label>
        <input type="date" name="date_to" id="date_to" value={form.date_to.value} />
      </div>
      <div>
        <label htmlFor="income_type">{form.fields.income_type.label}</label>
        <select id="income_type" name="income_type">
          {form.fields.income_type.choices.map(([value, text]) => (
            <option key={value} value={value} selected={form.income_type.value === value}>{text}</option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="total_amount">Total amount</label>
        <input disabled type="number" id="total_amount" value={total_amount} />
      </div>
    </form>

    {object_list.length > 0 ? (
      <table className="listing">
        <thead>
          <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Order</th>
          </tr>
        </thead>
        <tbody>
          {object_list.map(order => (
            <tr key={order.id}>
              <td className="title" valign="top">{order.date_created}</td>
              <td className="status" valign="top">{order.total} ₪</td>
              <td>{order.extra.replenishment_amount ? 'Balance replenishment' : 'Purchase'}</td>
              <td valign="top"><a href={`/admin/shop/order/edit/${order.id}/`}>{order.ref}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    ) : (
      <p>No pages found.</p>
    )}
  </div>
);

export default EarningReport;
```

שים לב שהקוד הזה מניח שכל הנתונים מגיעים כמאפיינים לקומפוננטה. אם הנתונים מגיעים ממקור אחר (למשל, מ־API או ממסד נתונים), תצטרך להתאים את הקוד למקור הנתונים שלך.