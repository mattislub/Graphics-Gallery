ב־Next.js, אנחנו משתמשים ב־React כדי ליצור קומפוננטות. הקוד הבא הוא המרה של הקוד שלך לקומפוננטת React שתתאים ל־Next.js:

```jsx
import Image from 'next/image';
import { useRouter } from 'next/router';
import { getCategories } from '../lib/api';
import Category from '../components/Category';

export default function CategoriesPage({ categories }) {
  const router = useRouter();

  return (
    <div>
      <Image src={categories.image} alt="categories" className="rounded-lg mx-auto" />
      <SearchBlock changeUrl={false} />
      <div className="container grow mt-12 text-blue">
        <div className="mx-2.5">
          <div className="flex gap-2.5 justify-center items-center">
            <div className="border-2 border-blue rounded-full p-1 hidden sm:block">
              {/* SVG */}
            </div>
            <h1 className="text-2xl sm:text-4xl md:text-7xl font-black text-center ">{categories.title}</h1>
            <div className="border-2 border-blue rounded-full p-1 hidden sm:block">
              {/* SVG */}
            </div>
          </div>
          <div className="mt-12 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 sm:gap-5" style={{direction: 'rtl'}}>
            {categories.map((category) => (
              <Category key={category.id} category={category} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export async function getStaticProps() {
  const categories = await getCategories();
  return {
    props: {
      categories,
    },
  };
}
```

הערות:
- אני מניח שיש לך קומפוננטה בשם `SearchBlock` שמטפלת בחיפוש.
- אני מניח שיש לך קומפוננטה בשם `Category` שמטפלת בהצגת קטגוריה.
- אני מניח שיש לך פונקציה בשם `getCategories` שמביאה את כל הקטגוריות.
- הסימנים `{/* SVG */}` הם מקום שבו אתה יכול להוסיף את הקוד של ה־SVG שלך.
- הפונקציה `getStaticProps` משמשת לטעינת הנתונים בזמן בנייה. אם אתה מעדיף לטעון את הנתונים בזמן ריצה, אתה יכול להשתמש בפונקציה `getServerSideProps` במקום.