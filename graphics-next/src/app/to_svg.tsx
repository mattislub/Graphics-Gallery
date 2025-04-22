אתה מבקש להמיר קובץ תבנית Django ל-Next.js. זה יכול להיות מורכב מאוד מכיוון ש-Next.js משתמש ב-JavaScript ו-React, בעוד Django משתמש ב-Python ותבניות Django. אני אציג דוגמה של איך הקובץ יכול להיראות ב-Next.js, אך שים לב שזה יכול לדרוש שינויים נוספים בהתאם לקוד הספציפי שלך.

```jsx
import { useState } from 'react';

export default function ToSvg() {
    const [presets, setPresets] = useState({
        'B&W': {
            'color_mode': 'binary',
            'mode': 'spline',
            'filter_speckle': '4',
            'color_precision': '6',
            'layer_difference': '16',
            'corner_threshold': '60',
            'length_threshold': '4.0',
            'splice_threshold': '45',
            'path_precision': '2'
        },
        'Poster': {
            'color_mode': 'color',
            'mode': 'spline',
            'filter_speckle': '4',
            'color_precision': '8',
            'layer_difference': '16',
            'corner_threshold': '60',
            'length_threshold': '4.0',
            'splice_threshold': '45',
            'path_precision': '2'
        },
        'Photo': {
            'color_mode': 'color',
            'mode': 'spline',
            'filter_speckle': '10',
            'color_precision': '8',
            'layer_difference': '48',
            'corner_threshold': '180',
            'length_threshold': '4.0',
            'splice_threshold': '45',
            'path_precision': '2'
        }
    });

    // ... קוד נוסף ...

    return (
        <div className="container grow mt-12 text-blue">
            <form 
                method="POST"
                enctype="multipart/form-data"
                className="mx-2.5 flex gap-2.5 flex-wrap sm:flex-nowrap">
                {/* ... קוד נוסף ... */}
            </form>
        </div>
    );
}
```

שים לב שהקוד הזה הוא רק דוגמה ויכול לדרוש שינויים נוספים כדי להתאים לקוד שלך. במיוחד, קוד ה-JavaScript שמוסיף אירועים לאלמנטים ומבצע בקשות fetch יצטרך להיכתב באמצעות hooks של React כמו useEffect. בנוסף, קוד התבנית של Django שמציג את הטופס וההודעות יצטרך להיכתב באמצעות JSX.