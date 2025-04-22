הקובץ המרוכז של Next.js יראה כך:

./components/SearchBlock.js

התוכן:
-----
```jsx
import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import { getSelectedImageCategory, getSearchText, getImageCategories, getSortingOptions, getImageOrientations, getUserSubscriptions } from '../lib/api';

export default function SearchBlock({ changeUrl }) {
    const router = useRouter();
    const [searchString, setSearchString] = useState('');
    const [imageCategory, setImageCategory] = useState('all');
    const [imageOrientation, setImageOrientation] = useState('all');
    const [imageFilter, setImageFilter] = useState('all');
    const [sortBy, setSortBy] = useState('popular');
    const [initialized, setInitialized] = useState(false);

    useEffect(() => {
        if (!initialized) {
            initialize();
        } else if (changeUrl) {
            search();
        }
    }, [imageCategory, imageOrientation, imageFilter, sortBy]);

    const search = () => {
        let url = new URL(router.pathname, window.location.href);
        let params = new URLSearchParams(url.search);

        if (searchString) params.append('search', searchString);
        if (imageCategory !== 'all') params.append('image-category', imageCategory);
        if (imageOrientation !== 'all') params.append('image-orientation', imageOrientation);
        if (imageFilter === 'premium') params.append('premium', true);
        if (imageFilter === 'usual') params.append('usual', true);
        if (imageFilter === 'free') params.append('free', true);
        if (sortBy !== 'popular') params.append('sort-by', sortBy);

        url.search = params.toString();
        window.location = url.toString();
    };

    const initialize = () => {
        let url = new URL(window.location.href);
        let params = new URLSearchParams(url.search);

        if (params.has('premium')) setImageFilter('premium');
        if (params.has('usual')) setImageFilter('usual');
        if (params.has('free')) setImageFilter('free');
        if (params.has('sort-by')) setSortBy(params.get('sort-by'));
        if (params.has('image-orientation')) setImageOrientation(params.get('image-orientation'));
        if (params.has('image-category')) setImageCategory(params.get('image-category'));

        setInitialized(true);
    };

    return (
        <div id="search_block" className="z-10">
            {changeUrl && (
                <div className="mx-6 mt-5">
                    {getSelectedImageCategory() ? (
                        <div className="py-36 rounded-2xl bg-cover bg-center" style={{ backgroundImage: `url(${getSelectedImageCategory().display_image.url})` }}>
                            <div className="flex gap-2.5 justify-center items-center">
                                <div className="border-2 border-blue rounded-full p-1 hidden sm:block">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="72" height="17" viewBox="0 0 72 17" fill="none">
                                        <path d="M0.399789 9.41385L0.401009 9.41514L7.5218 16.5016C8.05526 17.0325 8.91811 17.0305 9.44912 16.497C9.98005 15.9635 9.97801 15.1007 9.44455 14.5697L4.66364 9.81199L69.999 9.81199C70.7517 9.81199 71.3618 9.20188 71.3618 8.44921C71.3618 7.69655 70.7517 7.08644 69.999 7.08644L4.66371 7.08643L9.44449 2.32869C9.97794 1.79775 9.97999 0.934911 9.44905 0.401451C8.91804 -0.132145 8.05513 -0.133983 7.52174 0.396818L0.400941 7.48327L0.39972 7.48456C-0.13401 8.01727 -0.132308 8.88291 0.399789 9.41385Z" fill="currentColor"/>
                                    </svg>
                                </div>
                                <h1 className="text-2xl sm:text-4xl md:text-7xl font-black text-center">{getSelectedImageCategory().name} Category</h1>
                                <div className="border-2 border-blue rounded-full p-1 hidden sm:block">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="72" height="17" viewBox="0 0 72 17" fill="none">
                                        <path xmlns="http://www.w3.org/2000/svg" d="M71.6007 7.58616L71.5995 7.58486L64.4787 0.49841C63.9452 -0.0324602 63.0824 -0.0304848 62.5514 0.503043C62.0204 1.0365 62.0225 1.89935 62.5559 2.43029L67.3368 7.18802L2.00146 7.18801C1.2488 7.18801 0.638686 7.798