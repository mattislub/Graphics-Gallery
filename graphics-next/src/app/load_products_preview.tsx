ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) וב-React ליצירת הממשק המשתמש, ולא בתבניות Django. הנה דוגמה לקובץ שממש את אותו התוכן ב-Next.js:

```jsx
import { useState } from 'react';

export default function LoadProductsPreview({ categories }) {
  const [images, setImages] = useState(null);
  const [category, setCategory] = useState('');
  const [sellingOption, setSellingOption] = useState('usual');
  const [price, setPrice] = useState(0.00);

  const handleSubmit = (event) => {
    event.preventDefault();
    // TODO: Handle form submission
  };

  return (
    <div>
      <h1>Multiple Product Loading</h1>
      <div className="nice-padding">
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <div className="w-panel">
            <h2>Zip file with images *</h2>
            <input type="file" accept=".zip" onChange={(e) => setImages(e.target.files[0])} />
          </div>
          <div className="w-panel">
            <h2>Category *</h2>
            <select style={{ width: '100%' }} onChange={(e) => setCategory(e.target.value)}>
              {categories.map((category) => (
                <option key={category.slug} value={category.slug}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          <div className="w-panel">
            <h2>Selling option *</h2>
            <select style={{ width: '100%' }} onChange={(e) => setSellingOption(e.target.value)}>
              <option value="usual">Usual</option>
              <option value="premium">Premium</option>
              <option value="subscription">Subscription</option>
            </select>
          </div>
          <div className="w-panel">
            <h2>Price *</h2>
            <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
          </div>
          <input type="submit" value="Save" className="button" />
        </form>
      </div>
    </div>
  );
}

// TODO: Fetch categories from server
export async function getServerSideProps() {
  const categories = []; // Replace with actual data fetching

  return {
    props: {
      categories,
    },
  };
}
```

שים לב שאנחנו צריכים להוסיף את הקוד שמבצע את הבקשה לשרת כדי לקבל את הקטגוריות. זה יכול להיעשות בפונקציה `getServerSideProps`.