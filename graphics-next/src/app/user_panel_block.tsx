התוכן הממומש ב-React.js ו-Next.js:
-----
```jsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { getSortOptions, getImageOrientations, getImageCategories } from '../api'; // יש להוסיף את הפונקציות האלה בקובץ ה- API שלך

export default function UserPanelBlock({ showSearchBlock }) {
  const router = useRouter();
  const [searchString, setSearchString] = useState('');
  const [imageCategory, setImageCategory] = useState('all');
  const [imageOrientation, setImageOrientation] = useState('all');
  const [imageFilter, setImageFilter] = useState('all');
  const [sortBy, setSortBy] = useState('popular');

  const search = () => {
    const params = new URLSearchParams();

    if (searchString) params.append('search', searchString);
    if (imageCategory !== 'all') params.append('image-category', imageCategory);
    if (imageOrientation !== 'all') params.append('image-orientation', imageOrientation);
    if (imageFilter ===