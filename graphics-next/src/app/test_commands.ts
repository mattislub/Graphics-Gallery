אז למרות ש-Next.js הוא סביבת פיתוח ב-JavaScript, אני אנסה להמיר את הקוד שלך מ-Python ל-JavaScript. אני מניח שאתה מנסה לבדוק את פונקציונליות ה-DB שלך, אז אני אשתמש במודול 'pg' של Node.js להתממשקות עם PostgreSQL.

אני מניח שאתה מנסה לבדוק את פונקציונליות ה-DB שלך, אז אני אשתמש במודול 'pg' של Node.js להתממשקות עם PostgreSQL.

```javascript
// ./app/core/tests/test_commands.js

const { Client } = require('pg');
const sleep = require('util').promisify(setTimeout);

class CommandTests {
  constructor() {
    this.client = new Client({
      // your db config here
    });
    this.client.connect();
  }

  async check() {
    try {
      await this.client.query('SELECT NOW()');
      return true;
    } catch (err) {
      return false;
    }
  }

  async waitForDb() {
    let isDbReady = await this.check();
    let attempts = 0;

    while (!isDbReady && attempts < 5) {
      await sleep(1000);
      isDbReady = await this.check();
      attempts++;
    }

    return isDbReady;
  }
}

// tests
(async () => {
  const commandTests = new CommandTests();

  console.log(await commandTests.waitForDb()); // should return true if DB is ready

  // simulate DB not ready
  commandTests.client.end();
  console.log(await commandTests.waitForDb()); // should return false
})();
```

אני מקווה שזה עוזר! שים לב שזה רק דוגמה ואתה תצטרך להתאים את הקוד לצרכים שלך.