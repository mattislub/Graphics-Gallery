הקובץ שלך משתמש בתבנית Django, אך Next.js משתמש ב-React.js להצגת ממשק המשתמש. כדי להמיר את הקובץ ל-Next.js, תצטרך להמיר את התבנית לקומפוננטת React. הנה דוגמה לקובץ שהומר ל-Next.js:

./app/salesman_admin/components/ChangeForm.js

התוכן:
-----
```jsx
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'

const ChangeForm = ({ original }) => {
  const router = useRouter()
  const [orderRefundUrl, setOrderRefundUrl] = useState(null)

  useEffect(() => {
    // Replace with your actual function to get the refund URL.
    const fetchRefundUrl = async () => {
      const url = await fetch(`/admin/shop_order_refund/${original.id}`)
      setOrderRefundUrl(url)
    }

    fetchRefundUrl()
  }, [original.id])

  return (
    <>
      {orderRefundUrl && (
        <div className="submit-row">
          <a href={orderRefundUrl} className="button">Refund order</a>
        </div>
      )}

      {/* Add your other form fields here. */}
    </>
  )
}

export default ChangeForm
```
-----

שים לב שהקוד המעלה מניח שיש לך פונקציה שמחזירה את ה-URL להחזר הכספי עבור ההזמנה. תצטרך להחליף את הפונקציה `fetchRefundUrl` בפונקציה המתאימה לאפליקציה שלך.