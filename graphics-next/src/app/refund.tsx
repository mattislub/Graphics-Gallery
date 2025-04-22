ב-Next.js, אנחנו משתמשים ב-JSX במקום בתבניות Django. נצטרך להמיר את התבנית לקומפוננטת React. נניח שכל הקומפוננטות הנדרשות כבר מוגדרות, הקובץ המומר יראה כך:

./app/salesman_admin/components/Refund.js
```jsx
import { useRouter } from 'next/router'
import Head from 'next/head'
import Breadcrumbs from './Breadcrumbs'
import RefundContent from './RefundContent'

const Refund = ({ object, opts, media }) => {
  const router = useRouter()

  const objectUrl = `${opts.app_label}/${opts.verbose_name_plural}/${object.pk}`

  return (
    <>
      <Head>
        {media}
        <script src="/salesman/admin/includes/refund.js"></script>
      </Head>

      <Breadcrumbs>
        <a href={router.pathname}>{'Home'}</a>
        <a href={`${opts.app_label}`}>{opts.app_config.verbose_name}</a>
        <a href={`${opts.app_label}/${opts.verbose_name_plural}`}>{opts.verbose_name_plural}</a>
        <a href={objectUrl}>{object.name}</a>
        {'Refund'}
      </Breadcrumbs>

      <RefundContent objectUrl={objectUrl} />
    </>
  )
}

export default Refund
```
שים לב שהקוד מניח שיש לך קומפוננטות `Breadcrumbs` ו-`RefundContent` שמטפלות בהצגת הפרטים המתאימים. כמו כן, זה מניח שאתה מעביר את `object`, `opts` ו-`media` כמאפיינים לקומפוננטה. אתה יכול להתאים את הקוד לצרכים שלך.