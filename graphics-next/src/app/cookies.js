ב־Next.js, אנחנו משתמשים ב־API של השרת כדי להגדיר ולקבל עוגיות. לכן, נצטרך להפוך את הפונקציות שלנו ל־API Routes. נצטרך גם להשתמש ב־cookies מהחבילה של 'cookie' כדי להגדיר ולקבל עוגיות.

הנה דוגמה לקובץ API Route שמגדיר עוגיה:

./pages/api/setCookie.js
-----
import { serialize } from 'cookie'

export default function handler(req, res) {
  const name = req.body.name
  const value = req.body.value
  const options = req.body.options || {}

  if (!options.expires) {
    options.expires = new Date('9999-12-31T23:59:59Z');
  }

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  res.setHeader('Set-Cookie', serialize(name, JSON.stringify(value), options))
  res.status(200).json({ message: 'Cookie set' })
}
-----

הנה דוגמה לקובץ API Route שמחזיר עוגיה:

./pages/api/getCookie.js
-----
import { parse } from 'cookie'

export default function handler(req, res) {
  const name = req.body.name
  const cookies = parse(req.headers.cookie || '')
  const value = cookies[name]

  res.status(200).json({ value: value ? JSON.parse(value) : undefined })
}
-----

הנה דוגמה לקובץ API Route שמוחק עוגיה:

./pages/api/deleteCookie.js
-----
import { serialize } from 'cookie'

export default function handler(req, res) {
  const name = req.body.name

  res.setHeader('Set-Cookie', serialize(name, '', { 'max-age': -1 }))
  res.status(200).json({ message: 'Cookie deleted' })
}
-----

אתה יכול לקרוא ל־API Routes האלה מהקוד שלך באמצעות fetch או axios.