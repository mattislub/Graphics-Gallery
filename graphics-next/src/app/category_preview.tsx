ב־Next.js, אנחנו משתמשים ב־React כדי ליצור קומפוננטות. ניתן להמיר את הקובץ שלך לקומפוננטת React כך:

```jsx
import Image from 'next/image';

function CategoryPreview({ category }) {
  return (
    <div className="flex flex-col items-center group cursor-pointer" onClick={() => updateURLParameter('image-category', category.slug)}>
      <div className="border-2 border-white rounded-full group-hover:border-blue">
        <Image src={category.small_preview_image} alt={category.name} width={200} height={200} className="w-40 rounded-full" />
      </div>
      <p className="text-xl text-blue font-normal">{category.name}</p>
    </div>
  );
}

export default CategoryPreview;
```

הערות:
1. יש להתקין את הספרייה `next/image` כדי להשתמש בקומפוננטת `Image`.
2. הפונקציה `updateURLParameter` צריכה להיות מוגדרת או מיובאת ממקום אחר.
3. אני מניח ש־`category` הוא אובייקט שמגיע כמאפיין לקומפוננטה. אם זה לא המקרה, תצטרך להתאים את הקוד בהתאם.
4. ניתן להוסיף את הקובץ הזה לתיקיית `components` בפרויקט שלך, ולייבא אותו משם לקומפוננטות אחרות שמשתמשות בו.