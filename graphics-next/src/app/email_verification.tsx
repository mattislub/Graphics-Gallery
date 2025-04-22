ב-Next.js, אנחנו נשתמש ב-JSX וב-React כדי ליצור קומפוננטות. נשתמש גם ב-React hooks כדי לטעון מידע דינמי. נניח שיש לנו hook בשם useSiteData שמחזיר את המידע שאנחנו צריכים. הקוד המרוקח יראה כך:

```jsx
import { useSiteData } from '../hooks';

export default function EmailVerification({ verificationCode }) {
  const { siteName, rootUrl, contactUsUrl } = useSiteData();

  return (
    <div>
      <table style={{ margin: '0 auto', color: '#030339', maxWidth: '400px', padding: '10px', borderRadius: '20px', backgroundColor: '#C6C6D1' }}>
        <tr>
          <td>
            <table style={{ marginLeft: 'auto', color: '#030339', fontSize: '30px', fontWeight: '900' }}>
              <tr>
                <td>{siteName}</td>
                <td>
                  <img style={{ height: '60px' }} src={`${rootUrl}/static/media/logo.png`} alt={siteName} />
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }}>
            <div style={{ padding: '10px', borderRadius: '20px', textAlign: 'center', fontWeight: '900', fontSize: '36px' }}>
              Your verification code
            </div>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'right', fontSize: '20px' }}>
            Someone provided this email address to register for an account on {siteName}.
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px' }} align="center">
            <div style={{ display: 'inline-block', padding: '10px', borderRadius: '20px', backgroundColor: '#030339', color: 'white', textAlign: 'center', fontWeight: '900', fontSize: '36px', letterSpacing: '5px' }}>
              {verificationCode}
            </div>
          </td>
        </tr>
        <tr>
          <td style={{ paddingTop: '20px', textAlign: 'right', fontSize: '20px' }}>
            When prompted, enter this code to confirm that you have access to the specified email address.<br /><br />
            If you received this message by mistake, please ignore it.<br /><br />
            Sincerely, {siteName}.
          </td>
        </tr>
      </table>
      <table style={{ margin: '0 auto', color: '#646484', width: '400px' }}>
        <tr>
          <td style={{ paddingTop: '10px', textAlign: 'right', fontSize: '16px' }}>
            Do not reply to this message.<br />
            If you have any questions, please <a href={contactUsUrl}>contact us</a>.
          </td>
        </tr>
      </table>
    </div>
  );
}
```

אני מניח שיש לך hook בשם useSiteData שמחזיר את המידע הנדרש. אם אין לך אחד כזה, תצטרך ליצור אחד או להשתמש במקור מידע אחר.