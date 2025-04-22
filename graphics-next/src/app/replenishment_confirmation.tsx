ב־Next.js, אנחנו משתמשים בקומפוננטות React במקום תבניות Django. ניתן להשתמש בספריות כמו react-i18next לתרגום ובספריות כמו next/image לטעינת תמונות. ניתן להשתמש בפרופס להעברת משתנים לקומפוננטה.

הנה דוגמה לקובץ שהומר לקומפוננטת React שתתאים ל־Next.js:

```jsx
import Image from 'next/image'
import { useTranslation } from 'next-i18next'

export default function ReplenishmentConfirmation({ currentSite, user, order }) {
  const { t } = useTranslation()

  return (
    <div>
      <table>
        <tr>
          <td>{currentSite.site_name}</td>
          <td>
            <Image src={`${currentSite.root_url}/static/static/media/logo.png`} alt={currentSite.site_name} height={60} />
          </td>
        </tr>
      </table>
      <p>
        {t('Dear {{firstName}} {{lastName}}, We are pleased to inform you that your balance has been successfully replenished.', { firstName: user.first_name, lastName: user.last_name })}
      </p>
      <div>
        {t('Details')}
      </div>
      <table>
        <tr>
          <td>{order.total} ₪</td>
          <td>{t('Paid amount:')}</td>
        </tr>
        <tr>
          <td>{order.extra.replenishment_amount} ₪</td>
          <td>{t('Balance:')}</td>
        </tr>
      </table>
      <p>
        {t('Thank you for choosing our service. Sincerely, {{siteName}}.', { siteName: currentSite.site_name })}
      </p>
      <p>
        {t('Do not reply to this message. If you have any questions, please contact us.')}
      </p>
    </div>
  )
}
```

אני מניח שהקובץ נמצא בתיקייה `pages/email` ושהוא מיובא ומשמש באפליקציה שלך. אני מניח גם שהגדרת את המחרוזות לתרגום בקובץ i18n שלך.

אני ממליץ להשתמש בספריות כמו styled-components או emotion לסגנון הקומפוננטות שלך במקום להשתמש בסגנון מוטמע.