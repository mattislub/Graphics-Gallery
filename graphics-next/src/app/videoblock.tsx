ב־Next.js, אנחנו משתמשים ב־React כדי ליצור קומפוננטות. ניתן להמיר את התבנית שלך לקומפוננטת React כך:

```jsx
import React from 'react';

const VideoBlock = ({ video, title, text, icon, counter, videoPosition }) => (
  <div className={`flex flex-wrap sm:flex-nowrap gap-5 ${counter % 2 === 0 ? 'ml-5 sm:ml-10 md:ml-20' : 'mr-5 sm:mr-10 md:mr-20'}`}>
    {videoPosition === 'left' && (
      <div className="h-auto min-h-20 basis-full sm:basis-1/4 flex items-center mx-auto">
        <video loop className="w-full h-fill border-2 rounded-2xl border-blue" autoPlay muted>
          <source src={video.url} type="video/mp4" />
        </video>
      </div>
    )}
    <div className="flex gap-5 grow bg-blue bg-opacity-10 p-5 rounded-2xl justify-end">
      <div className="mt-auto">
        <h3 className="font-bold text-2xl sm:text-4xl text-right">{title}</h3>
        <div className="mt-3.5 text-end text-2xl sm:text-4xl">{text}</div>
      </div>
      <div className="flex flex-col gap-7">
        <div className="p-2 rounded-2xl border-2 border-blue pulse" style={{ color: `#${icon.icon_color}` }}>
          <svg className="w-11 h-11">{/* Add your SVG icon here */}</svg>
        </div>
        <div className="mt-auto p-2 rounded-2xl border-2 border-blue text-center text-4xl md:text-7xl animate-bounce">
          {counter}
        </div>
      </div>
    </div>
    {videoPosition === 'right' && (
      <div className="h-auto min-h-20 basis-full sm:basis-1/4 flex items-center mx-auto">
        <video loop className="w-full h-fill border-2 rounded-2xl border-blue" autoPlay muted>
          <source src={video.url} type="video/mp4" />
        </video>
      </div>
    )}
  </div>
);

export default VideoBlock;
```

שים לב שאני מניח שהנתונים יגיעו כמאפיינים לקומפוננטה. כמו כן, הקוד הזה מניח שאתה מטפל בהכנסת האייקון SVG באופן ידני. אם יש לך קומפוננטה נפרדת לאייקונים, תוכל להשתמש בה במקום הקוד ההערה.