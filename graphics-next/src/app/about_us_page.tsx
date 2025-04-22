ב־Next.js, אנחנו משתמשים בקומפוננטות React במקום תבניות Django. הנה דוגמה לקובץ שמראה איך יכול להיראות הקובץ המומר:

./pages/about_us_page.js
```jsx
import Image from 'next/image'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

export default function AboutUsPage({ page }) {
  const { t } = useTranslation('common')

  return (
    <div>
      <div id="about-us-block" className="min-h-[92vh] bg-center bg-no-repeat bg-cover mt-12" style={{ backgroundImage: `url(${page.about_us_image})` }}>
        <div className="container">
          <div className="mx-2.5">
            <h1 className="mt-[15vh] text-center text-white text-[50px] sm:text-[70px] md:text-[90px] font-extrabold leading-[100%] tracking-[3px]">{page.title}</h1>
            <div className="flex justify-end my-24">
              <div className="basis-full sm:basis-2/3 mx-5">
                <h2 className="text-white font-bold leading-relaxed tracking-widest text-2xl text-end">{t('About us')}</h2>
                <p className="text-white text-base font-bold leading-tight text-end tracking-widest">{page.about_us_description}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <h2 className="text-4xl font-bold leading-tight tracking-widest text-center mt-12">{page.about_us_detail_title}</h2>
      <div className="container mt-12 ">
        <div className="mx-2.5 flex justify-center flex-wrap gap-5">
          {page.detail_items.map((detail_item) => (
            <div key={detail_item.id} className="rounded-2xl max-w-80 bg-blue bg-opacity-10 border-2 border-blue p-5">
              <h3 className="font-bold text-center text-2xl leading-tight tracking-widest">{detail_item.title}</h3>
              <p className="mt-5 text-base font-normal text-center leading-7 tracking-wide">{detail_item.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export async function getServerSideProps({ locale }) {
  // Fetch data from external API
  const res = await fetch(`https://.../api/page`)
  const page = await res.json()

  // Pass data to the page via props
  return { props: { page, ...(await serverSideTranslations(locale, ['common'])) } }
}
```

שים לב שזה דוגמה בסיסית ואתה תצטרך להתאים את הקוד לצרכים שלך. לדוגמה, אתה תצטרך להחליף את הקישור בפונקציה `getServerSideProps` כדי לקבל את הנתונים מה־API שלך.