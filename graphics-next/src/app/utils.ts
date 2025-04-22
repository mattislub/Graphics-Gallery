אני מניח שאתה מעוניין להמיר את הקוד מ-Python ל-JavaScript כדי שהוא יתאים לפרויקט Next.js. הנה המרה אפשרית של הקובץ:

./app/salesman_admin/utils.js
-----
```javascript
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-json';
import appSettings from '../conf/appSettings';
import Order from '../orders/models/Order';

export function formatJson(value, context = {}) {
    let output = JSON.stringify(value, null, 2);
    output = highlight(output, languages.json, 'json');
    const styled = context.styled !== undefined ? context.styled : true;

    let html;
    if (styled) {
        html = `<style></style><pre class="highlight" style="margin: 0; padding: 1em;">${output}</pre>`;
    } else {
        html = `<pre style="margin: 0;">${output}</pre>`;
    }
    return `<div>${html}</div>`;
}

export function formatPrice(value, order, request) {
    const context = {
        request,
        order,
        admin: true,
    };
    return appSettings.SALESMAN_PRICE_FORMATTER(value, context);
}
```
-----
שים לב שהקוד המומר מניח שיש לך מודולים מתאימים בנתיבים שמוזכרים ב-imports. כמו כן, הפונקציה `highlight` מהספרייה `prismjs` משמשת כחלופה ל-`pygments_highlight` מ-Python. אני מניח שהגדרות האפליקציה והמודל `Order` מיובאים מנתיבים דומים לאלה שבקובץ ה-Python המקורי.