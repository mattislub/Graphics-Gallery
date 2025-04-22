קודם כל, נשים לב שהקובץ המקורי הוא קובץ Python שמשתמש ב־Django. ב־Next.js, שהוא סביבת Node.js, אנחנו משתמשים ב־JavaScript או ב־TypeScript. נניח שאנחנו משתמשים ב־JavaScript.

בנוסף, נשים לב שהקובץ המקורי משתמש במודלים של Django כדי לבצע שאילתות למסד הנתונים. ב־Next.js, אנחנו יכולים להשתמש בספריות שונות כדי לבצע שאילתות למסד הנתונים, כמו Prisma או Sequelize. נניח שאנחנו משתמשים ב־Prisma.

לסיום, נשים לב שהקובץ המקורי משתמש בתגיות תבנית של Django כדי להציג נתונים בתבנית. ב־Next.js, אנחנו משתמשים בקומפוננטות React כדי להציג נתונים.

לכן, המרת הקובץ תדרוש שינויים משמעותיים. הנה דוגמה לקובץ JavaScript שמשתמש ב־Prisma וב־React:

```jsx
import { PrismaClient } from '@prisma/client'
import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

const prisma = new PrismaClient()

export default function Search() {
  const router = useRouter()
  const [imageCategories, setImageCategories] = useState([])
  const [selectedImageCategory, setSelectedImageCategory] = useState(null)

  useEffect(() => {
    async function fetchImageCategories() {
      const categories = await prisma.imageCategory.findMany({
        where: { available: true },
        orderBy: { slug: 'asc' },
      })
      setImageCategories(categories)
    }

    fetchImageCategories()
  }, [])

  useEffect(() => {
    const imageCategorySlug = router.query['image-category']
    if (imageCategorySlug) {
      const selectedCategory = imageCategories.find(
        (category) => category.slug === imageCategorySlug
      )
      setSelectedImageCategory(selectedCategory)
    }
  }, [router.query, imageCategories])

  // ... כאן ניתן להוסיף פונקציות נוספות ולהציג את הנתונים באמצעות קומפוננטות React
}
```

שים לב שהקוד הזה הוא רק דוגמה ויכול להיות שתצטרך להתאים אותו לצרכים שלך.