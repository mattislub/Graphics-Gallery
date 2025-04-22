ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) וב-React ליצירת קומפוננטות ודפים. לכן, נצטרך להמיר את התבנית שלנו לקומפוננטת React. נניח שכל הפונקציות והמשתנים שאנחנו משתמשים בהם בתבנית זמינים לנו באופן מתאים ב-Next.js.

הנה דוגמה לקובץ שהומר ל-Next.js:

```jsx
import React from 'react';
import { useRouter } from 'next/router';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import RootPage from '../components/RootPage';
import SearchBlock from '../components/SearchBlock';
import CategoryPreview from '../components/CategoryPreview';
import ImageProduct from '../components/ImageProduct';

export default function ImagesPage({ childrenImageCategories, pageProducts, tagsList }) {
  const router = useRouter();
  const { t } = useTranslation('common');

  return (
    <RootPage>
      <SearchBlock changeUrl={true} />
      <div className="mx-6">
        {childrenImageCategories.length > 0 && (
          <div className="mt-12">
            <div className="mt-12 flex flex-wrap justify-end gap-5 border-t-2 pt-5 border-blue">
              {childrenImageCategories.map(category => (
                <CategoryPreview key={category.id} category={category} />
              ))}
            </div>
          </div>
        )}
      </div>
      <div className="container grow">
        <div className="mx-2.5">
          <div id="product-list-container" className="mt-12 flex flex-wrap gap-2.5 sm:gap-5">
            {pageProducts.map(product => (
              <ImageProduct key={product.id} product={product} />
            ))}
          </div>
          {/* Pagination code here */}
        </div>
      </div>
      <div id="relevant-tags" className="mt-12 container">
        <div className="mx-2.5">
          <h2 className="text-blue text-end text-4xl sm:text-7xl leading-none font-light flex items-center justify-end gap-2.5">
            {t('Relevant tags')}
          </h2>
          <div className="mt-12 flex flex-wrap gap-2.5 sm:gap-5" style={{ direction: 'rtl' }}>
            {tagsList.map(tag => (
              <a key={tag.name} href={`/images?search=${tag.name}`} className="border border-blue text-blue px-2 py-1 rounded-full hover:bg-blue hover:bg-opacity-30 hover:text-white hover:border-transparent">{tag.name}</a>
            ))}
          </div>
        </div>
      </div>
    </RootPage>
  );
}

export async function getServerSideProps({ locale }) {
  // Fetch data from server
  const childrenImageCategories = []; // Replace with actual data
  const pageProducts = []; // Replace with actual data
  const tagsList = []; // Replace with actual data

  return {
    props: {
      ...await serverSideTranslations(locale, ['common']),
      childrenImageCategories,
      pageProducts,
      tagsList,
    },
  };
}
```

שים לב שהקוד הזה מניח שיש לך קומפוננטות React מתאימות עבור `RootPage`, `SearchBlock`, `CategoryPreview` ו-`ImageProduct`. כמו כן, זה מניח שאתה משתמש ב-`next-i18next` עבור תרגום. 

החלק של הפגינציה (Pagination) דורש יותר קוד ותלוי באיך אתה מנהל את הנתונים שלך, אז אני השארתי אותו ריק.