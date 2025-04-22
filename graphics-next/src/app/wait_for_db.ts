Next.js הוא סביבת פיתוח בג'אווה סקריפט ולא תומך בפייתון. על כן, אנחנו צריכים להמיר את הקוד לג'אווה סקריפט. כמו כן, Next.js משתמש ב-Prisma כדי להתממשק עם מסדי נתונים, ולא Django ORM. לכן, אנחנו צריכים להשתמש ב-Prisma במקום Django ORM.

הנה הגרסה המומרת של הקובץ:

```javascript
// ./app/core/management/commands/wait_for_db.js

/**
 * Next.js command to wait for the Database to be available.
 */

import { PrismaClient } from '@prisma/client';
import sleep from 'await-sleep';

const prisma = new PrismaClient();

async function waitForDb() {
  console.log("Run wait for Database...");
  let dbIsUp = false;
  while (!dbIsUp) {
    try {
      await prisma.$connect();
      dbIsUp = true;
    } catch (error) {
      console.log("Database unavailable...");
      await sleep(1000);
    }
  }
  console.log('Database available.');
}

waitForDb();
```

הקוד מנסה להתחבר למסד הנתונים כל שנייה עד שהחיבור מצליח. אם החיבור מצליח, הוא מסיים את הלולאה ומדפיס שהמסד נתונים זמין. אם החיבור נכשל, הוא ממתין שנייה ונסה שוב.