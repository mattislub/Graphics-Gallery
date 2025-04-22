ב־Next.js, אנחנו משתמשים בקומפוננטות React כדי ליצור ממשק משתמש. ניתן להשתמש בספריות כמו react-i18next לתמיכה ברב־לשוניות וב־next/image לטיפול בתמונות. נניח שיש לנו קומפוננטה שנקראת BasketItem שמציגה מוצרים בסל, ניתן להמיר את התבנית הנ"ל לקובץ JSX כך:

```jsx
import Image from 'next/image'
import { useTranslation } from 'react-i18next'
import BasketItem from './BasketItem'

export default function UnpaidBasketNotification({ currentSite, user, basket }) {
  const { t } = useTranslation()

  return (
    <>
      <style jsx>{`
        .button:hover{
            background-image: linear-gradient(90deg, #FA972A, #1939F8, #21FEC7);
        }
      `}</style>
      <table style={{ margin: '0 auto', color: '#030339', maxWidth: '400px', padding: '10px', borderRadius: '20px', backgroundColor: '#C6C6D1' }}>
        <tr>
          <td>
            <table style={{ marginLeft: 'auto', color: '#030339', fontSize: '30px', fontWeight: '900' }}>
              <tr>
                <td>{currentSite.siteName}</td>
                <td>
                  <Image height={60} src={`${currentSite.rootUrl}/static/static/media/logo.png`} alt={currentSite.siteName} />
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ textAlign: 'center', fontSize: '36px', fontWeight: '900' }}>
            {t('You have unpaid basket')}
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'end', fontSize: '20px' }}>
            {t('Dear {{user}},<br>We are pleased to inform you that you have unpaid basket items.', { user })}
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }}>
            <table style={{ padding: '10px', width: '100%', backgroundColor: '#030339', color: 'white', fontSize: '24px', fontWeight: '900' }}>
              <tr>
                <td style={{ textAlign: 'left' }}>{t('Price')}</td>
                <td style={{ textAlign: 'right' }}>{t('Product')}</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td>
            <table style={{ width: '100%', color: '#030339', fontSize: '20px' }}>
              {basket.items.map((basketItem) => (
                <BasketItem key={basketItem.product.code} basketItem={basketItem} />
              ))}
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }}>
            <table style={{ padding: '10px 0', borderTop: '2px solid #030339', borderBottom: '2px solid #030339', width: '100%', color: '#030339', fontSize: '24px', fontWeight: '900' }}>
              <tr>
                <td style={{ textAlign: 'left' }}>{basket.total} ₪</td>
                <td style={{ textAlign: 'right' }}>{t('Total')}</td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }} align="center">
            <div style={{ display: 'inline-block' }}>
              <a style={{ textDecoration: 'none' }} href="/basket">
                <table className="button" style={{ color: '#030339', padding: '5px', borderRadius: '20px', border: '2px solid #030339' }}>
                  <tr>
                    <td>
                      <div style={{ backgroundColor: '#030339', padding: '2px 4px', borderRadius: '10px' }}>
                        <Image width={16} src={`${currentSite.rootUrl}/static/static/media/heroicons_chevron-left.png`} alt="Button icon" />
                      </div>
                    </td>
                    <td>{t('View basket')}</td>
                  </tr>
                </table>
              </a>
            </div>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'right', fontSize: '20px' }}>
            {t('Thank you for choosing our service.<br><br>Sincerely, {{siteName}}.', { siteName: currentSite.siteName })}
          </td>
        </tr>
      </table>
      <table style={{ margin: '0 auto', color: '#646484', width: '400px' }}>
        <tr>
          <td style={{ paddingTop: '10px', textAlign: 'right', fontSize: '16px' }}>
            {t('Do not reply to this message.<br>If you have any questions, please <a href="{{url}}">contact us</a>.', { url: '/contact-us' })}
          </td>
        </tr>
      </table>
    </>
  )
}
```

שים לב שהקוד הזה מניח שיש לך קומפוננטה שנקראת BasketItem שמציגה מוצרים בסל. אם אין לך קומפוננטה כזו, תצטרך ליצור אחת או להציג את המוצרים באופן אחר.