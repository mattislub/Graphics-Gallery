ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) וב-React ליצירת קומפוננטות. ניתן להמיר את הקובץ הנ"ל לקומפוננטת React כך:

```jsx
// ./components/Category.js
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';

export default function Category({ category }) {
    const { t } = useTranslation();
    const router = useRouter();

    return (
        <div className="roundex-3xl relative h-40 sm:h-60 group" style={{ direction: 'ltr' }}>
            <div className="rounded-3xl h-full w-full">
                <Image className="object-cover h-full w-full rounded-3xl bg-white" src={category.preview_image} alt={category.name} />
            </div>
            <div className="absolute inset-0 rounded-3xl bg-gradient-to-t from-15% from-blue p-5 group-hover:from-45%">
                <div className="flex flex-col items-center text-lg text-white text-center h-full">
                    <p className="mt-auto text-3xl font-bold">{category.name}</p>
                    <a onClick={() => router.push(`/images?image-category=${category.slug}`)} target="_blank" className="mt-2.5 flex gap-4 items-center rounded-full font-bold text-lg bg-white bg-opacity-40 text-white py-2 px-5 group-hover:bg-opacity-100 group-hover:text-blue">
                        <div className="rounded-full border-2 py-0.5 px-5 text-white border-white group-hover:bg-blue">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                            </svg>
                        </div>
                        {t('Open category')}
                    </a>
                </div>
            </div>
        </div>
    );
}
```

אני מניח ש- `category` הוא אובייקט שמכיל את המאפיינים `preview_image`, `name` ו- `slug`. ניתן להעביר את האובייקט `category` כמאפיין לקומפוננטה כאשר אתה משתמש בה.

בנוסף, אני מניח שיש לך קובץ תרגום שמכיל את המחרוזת 'Open category'. אם אתה משתמש ב- `next-i18next`, אתה יכול להשתמש ב- `useTranslation` כדי לתרגם מחרוזות בקוד שלך.