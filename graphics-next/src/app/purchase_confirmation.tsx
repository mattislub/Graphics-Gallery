ב־Next.js, אנחנו משתמשים בקומפוננטות React כדי ליצור תבניות. ניתן להשתמש בספריות כמו i18next כדי לתמוך בתרגום ובספריות כמו next/image כדי להטמיע תמונות. נניח שיש לנו קובץ נתונים שמכיל את כל המידע שנדרש להזמנה.

הנה דוגמה לקובץ שיכול להחליף את התבנית שלך:

```jsx
import { useTranslation } from 'next-i18next';
import Image from 'next/image';
import orderData from './orderData.json';

export default function PurchaseConfirmation() {
  const { t } = useTranslation();

  return (
    <div>
      <table>
        <tr>
          <td>{orderData.siteName}</td>
          <td>
            <Image src="/logo.png" alt={orderData.siteName} width={60} height={60} />
          </td>
        </tr>
        <tr>
          <td>
            <Image src="/heroicons_check-circle.png" alt="Successful purchase" width={150} height={150} />
          </td>
        </tr>
        <tr>
          <td>{t('Thank you for your purchase')}</td>
        </tr>
        <tr>
          <td>
            {t('This email confirms that your order has been successfully paid. Order REF: {{orderRef}}.', { orderRef: orderData.orderRef })}
          </td>
        </tr>
        <tr>
          <td>{t('Price')}</td>
          <td>{t('Product')}</td>
        </tr>
        {orderData.items.map((item) => (
          <tr key={item.id}>
            <td>{item.price}</td>
            <td>{item.code}</td>
          </tr>
        ))}
        <tr>
          <td>{orderData.total}</td>
          <td>{t('Total')}</td>
        </tr>
        <tr>
          <td>
            {t('Thank you for choosing our service. Sincerely, {{siteName}}.', { siteName: orderData.siteName })}
          </td>
        </tr>
      </table>
      <table>
        <tr>
          <td>
            {t('Do not reply to this message. If you have any questions, please contact us.')}
          </td>
        </tr>
      </table>
    </div>
  );
}
```

אני מניח שהקובץ orderData.json מכיל את כל המידע שנדרש להזמנה. אתה יכול להחליף את זה עם קריאת API או מקור נתונים אחר.