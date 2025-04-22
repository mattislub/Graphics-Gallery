ב־Next.js, נכון להשתמש ב־React במקום jQuery. לכן, עלינו להמיר את הקוד הנ"ל לקומפוננטת React. ניתן להשתמש ב־React hooks כמו useEffect ו־useState כדי להגיע לתוצאה דומה.

הנה דוגמה לקוד שמממש את הפונקציונליות הבסיסית של הקוד המקורי:

```jsx
import React, { useEffect, useState, useRef } from 'react';

const TwentyTwenty = ({ beforeImage, afterImage, defaultOffsetPct = 0.5 }) => {
  const [offset, setOffset] = useState(defaultOffsetPct);
  const containerRef = useRef();

  useEffect(() => {
    const handleResize = () => {
      // קוד להתאמת הסליידר לגודל החלון
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    const handleMouseMove = (e) => {
      const containerRect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - containerRect.left;
      const pct = x / containerRect.width;
      setOffset(pct);
    };
    containerRef.current.addEventListener('mousemove', handleMouseMove);
    return () => containerRef.current.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div ref={containerRef} style={{ position: 'relative', height: '100%', width: '100%' }}>
      <img src={beforeImage} style={{ position: 'absolute', width: '100%', height: '100%', clip: `rect(auto, auto, auto, ${offset * 100}%)` }} />
      <img src={afterImage} style={{ position: 'absolute', width: '100%', height: '100%', clip: `rect(auto, ${offset * 100}%, auto, auto)` }} />
    </div>
  );
};

export default TwentyTwenty;
```

שים לב שהקוד הזה הוא רק דוגמה ואינו מממש את כל האפשרויות של הקוד המקורי. תוכל להוסיף פונקציונליות נוספת כמו labels, אפשרות להזיז את הסליידר רק עם הידית, וכו'.