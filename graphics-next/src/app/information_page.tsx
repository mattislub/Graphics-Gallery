ב-Next.js, נשתמש בקומפוננטות React במקום תבניות Django. נצטרך להמיר את התגיות של Django לקוד JavaScript ולהשתמש בקומפוננטות React כדי להציג את התוכן.

הקובץ המומר יראה כך:

```jsx
import Image from 'next/image'
import { useRouter } from 'next/router'
import { useTranslation } from 'next-i18next'

export default function InformationPage({ page }) {
  const { t } = useTranslation()
  const router = useRouter()

  return (
    <div className="container grow mt-12 text-blue">
      <div className="mx-2.5">
        <Image className="mx-auto" src={page.image.url} alt="faq" />
        <h1 className="text-4xl font-black text-center mt-12 leading-9">{page.title}</h1>
        <div className="max-w-4xl flex flex-col mt-12 font-normal text-lg leading-5 mx-auto" style={{direction: 'rtl', listStyle: 'decimal !important'}}>
          {page.body.map((block, index) => (
            <div key={index}>{block}</div>
          ))}
        </div>
      </div>

      <a href="/" className="mt-12 mx-auto w-fit flex gap-4 items-center rounded-full font-bold text-lg border-2 border-blue bg-blue text-white py-2 px-5 hover:bg-gradient-2 group" role="link" type="submit">
        <div className="rounded-full border-2 py-0.5 px-5 bg-blue border-white group-hover:border-blue">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>
        </div>
        {t('To home page')}
      </a>
    </div>
  )
}
```

שים לב שהקוד מניח שיש לך תמיכה בתרגום עם `next-i18next` ושהנתונים מגיעים מה-props של הקומפוננטה. תצטרך להתאים את הקוד למבנה הנתונים שלך.