ב-Next.js, אנחנו משתמשים ב-JSX במקום בתבניות Django. ניתן להשתמש בקומפוננטות React כדי ליצור תבנית דומה. הנה דוגמה לקובץ שאתה מחפש:

```jsx
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

export default function SubscriptionConfirmation({ currentSite, user, order }) {
  const { t } = useTranslation('common');
  const router = useRouter();

  return (
    <>
      <table style={{ margin: '0 auto', color: '#030339', maxWidth: '400px', padding: '10px', borderRadius: '20px', backgroundColor: '#C6C6D1' }}>
        <tr>
          <td>
            <table style={{ marginLeft: 'auto', color: '#030339', fontSize: '30px', fontWeight: '900' }}>
              <tr>
                <td>{currentSite.site_name}</td>
                <td>
                  <img style={{ height: '60px' }} src={`${currentSite.root_url}/static/static/media/logo.png`} alt={currentSite.site_name} />
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'right', fontSize: '20px' }}>
            {t('dear', { firstName: user.first_name, lastName: user.last_name })}<br />
            {t('subscriptionConfirmation')}
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }}>
            <div style={{ padding: '10px', textAlign: 'end', fontWeight: '900', fontSize: '36px', borderBottom: '2px solid #030339' }}>
              {t('details')}
            </div>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }}>
            <table style={{ marginLeft: 'auto', color: '#030339' }}>
              <tr>
                <td style={{ fontSize: '24px' }}> {order.total} ₪ </td>
                <td style={{ fontSize: '24px', fontWeight: '900' }}> {t('paidAmount')} </td>
              </tr>
              <tr>
                <td style={{ fontSize: '24px' }}> {order.extra.subscription_downloads_remaining} {t('downloads')}  {order.extra.subscription_duration_days} {t('days')} {order.extra.subscription}</td>
                <td style={{ fontSize: '24px', fontWeight: '900' }}> {t('subscription')} </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'right', fontSize: '20px' }}>
            {t('thankYou', { siteName: currentSite.site_name })}
          </td>
        </tr>
      </table>
      <table style={{ margin: '0 auto', color: '#646484', width: '400px' }}>
        <tr>
          <td style={{ paddingTop: '10px', textAlign: 'right', fontSize: '16px' }}>
            {t('doNotReply')}<br />
            {t('contactUs', { url: router.asPath })}
          </td>
        </tr>
      </table>
    </>
  );
}

export async function getServerSideProps({ locale }) {
  return {
    props: {
      ...await serverSideTranslations(locale, ['common']),
    },
  };
}
```

אני מניח שיש לך קובץ תרגום עם מפתחות כמו 'dear', 'subscriptionConfirmation', 'details', 'paidAmount', 'downloads', 'days', 'subscription', 'thankYou', 'doNotReply', ו-'contactUs'. אם אתה רוצה להשתמש במשתנים אחרים, תצטרך להוסיף אותם לקובץ התרגום שלך.