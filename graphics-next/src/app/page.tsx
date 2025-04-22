// 📁 src/app/page.tsx
import React from 'react';
import HeroHeader from '@/components/HeroHeader';
import PageTitle from '@/components/PageTitle';
import SearchBlock from '@/components/SearchBlock';
import AdvertisingBlocks from '@/components/AdvertisingBlocks';
import PopularProducts from '@/components/PopularProducts';
import PopularCategories from '@/components/PopularCategories';
import LastAddedProducts from '@/components/LastAddedProducts';
import PopularQueries from '@/components/PopularQueries';

export default function Page() {
  return (
    <main className="relative -mt-28">
      <HeroHeader />

      <PageTitle
        title="כותרת ראשית"
        subtitle="תת־כותרת"
      />

      <SearchBlock />

      <div className="grow">
        <AdvertisingBlocks />

        <PopularProducts />
        <PopularCategories />

        <div className="mt-12 container">
          <div className="mx-2.5 flex flex-col gap-5">
            <div className="max-w-2xl self-end">
              <h2 className="text-blue text-end text-4xl sm:text-7xl leading-none font-bold ">
                המודל המושלם{' '}
                <span className="text-orange">למצוא</span>
                <div className="flex items-end justify-end gap-2.5">
                  <span className="border-2 border-blue rounded-full py-2 px-3.5 pulse">
                    {/* SVG כאן */}
                  </span>
                  התמונה שלך
                </div>
              </h2>
            </div>
          </div>
        </div>

        <LastAddedProducts />
        <PopularQueries />
      </div>
    </main>
  );
}
