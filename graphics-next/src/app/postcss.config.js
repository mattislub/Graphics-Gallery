הקובץ postcss.config.js יתאים כבר ל־Next.js כפי שהוא. Next.js מתמיך בפוסטCSS מהקופסה, ואתה יכול להשתמש בכל תוסף שאתה רוצה.

אם אתה רוצה להוסיף תמיכה ב־CSS Modules, תצטרך להוסיף את התוסף postcss-modules לקובץ התצורה שלך:

```javascript
module.exports = {
  plugins: {
    "postcss-import": {},
    "postcss-simple-vars": {},
    "postcss-nested": {},
    "postcss-modules": {
      generateScopedName: "[name]__[local]___[hash:base64:5]",
    },
  },
}
```

אם אתה רוצה להשתמש בתוספים של PostCSS בקבצים שלך, תצטרך להוסיף את הסיומת .module.css לקבצים שלך. לדוגמה, אם יש לך קובץ בשם styles.css, תצטרך לשנות את שמו ל־styles.module.css.