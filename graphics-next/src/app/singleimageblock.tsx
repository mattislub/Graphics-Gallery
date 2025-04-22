ב-Next.js, אנחנו משתמשים ב-JSX במקום בתבניות Django. כאן הוא הקובץ שהומר ל-JSX:

```jsx
import Image from 'next/image';
import { useState } from 'react';

export default function SingleImageBlock({ block }) {
  const [image, setImage] = useState(block.image);
  const imagePosition = block.image_position;
  const title = block.title;
  const text = block.text;
  const icon = block.icon;
  const iconColor = block.icon.icon_color;
  const counter = block.counter;

  return (
    <div className={`flex flex-wrap sm:flex-nowrap gap-5 ${!counter.first && !counter.last ? (counter % 2 === 0 ? 'ml-5 sm:ml-10 md:ml-20' : 'mr-5 sm:mr-10 md:mr-20') : ''}`}>
      {imagePosition === 'left' && (
        <div className="h-auto min-h-20 basis-full sm:basis-1/4 rounded-2xl bg-cover border-2 border-blue" style={{ backgroundImage: `url(${image.url})` }}></div>
      )}
      <div className="flex gap-5 grow bg-blue bg-opacity-10 p-5 rounded-2xl justify-end">
        <div className="mt-auto">
          <h3 className="font-bold text-2xl sm:text-4xl text-right">{title}</h3>
          <div className="mt-3.5 text-end text-2xl sm:text-4xl">{text}</div>
        </div>
        <div className="flex flex-col gap-7">
          <div className="p-2 rounded-2xl border-2 border-blue pulse" style={{ color: `#${iconColor}` }}>
            <svg className="w-11 h-11">{icon}</svg>
          </div>
          <div className="mt-auto p-2 rounded-2xl border-2 border-blue text-center text-4xl md:text-7xl animate-bounce">
            {counter}
          </div>
        </div>
      </div>
      {imagePosition === 'right' && (
        <div className="h-auto min-h-20 basis-full sm:basis-1/4 rounded-2xl bg-cover border-2 border-blue" style={{ backgroundImage: `url(${image.url})` }}></div>
      )}
    </div>
  );
}
```

שים לב שאני מניח שאתה מעביר את הנתונים לקומפוננטה כ-prop. אתה יכול להתאים את הקוד לצרכים שלך.