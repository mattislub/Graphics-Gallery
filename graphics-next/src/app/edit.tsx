ב-Next.js, אנחנו משתמשים ב-JavaScript (או TypeScript) וב-React ליצירת קומפוננטות. הקוד הבא הוא תרגום של התבנית שלך לקומפוננטת React:

```jsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import Field from '../components/Field';

export default function EditUser({ user, canDelete }) {
    const [tab, setTab] = useState('account');
    const router = useRouter();

    const handleSubmit = (event) => {
        event.preventDefault();
        // TODO: Handle form submission
    };

    const handleDelete = () => {
        // TODO: Handle user deletion
        router.push('/wagtailusers_users/delete/' + user.pk);
    };

    return (
        <div>
            <header>
                {/* TODO: Include shared header */}
            </header>

            <div className="w-tabs" data-tabs>
                <div className="w-tabs__wrapper">
                    <div role="tablist" className="w-tabs__list">
                        <button onClick={() => setTab('account')}>Account</button>
                        <button onClick={() => setTab('roles')}>Roles</button>
                    </div>
                </div>

                <form onSubmit={handleSubmit} noValidate>
                    <div className="tab-content">
                        {tab === 'account' && (
                            <section id="tab-account" className="w-tabs__panel" role="tabpanel" aria-labelledby="tab-label-account">
                                <ul className="fields">
                                    {/* TODO: Render form fields */}
                                    <li>
                                        <input type="submit" value="Save" className="button" />
                                        {canDelete && (
                                            <button onClick={handleDelete} className="button no">Delete user</button>
                                        )}
                                    </li>
                                </ul>
                            </section>
                        )}

                        {tab === 'roles' && (
                            <section id="tab-roles" className="w-tabs__panel" role="tabpanel" aria-labelledby="tab-label-roles">
                                <ul className="fields">
                                    {/* TODO: Render form fields */}
                                    <li>
                                        <input type="submit" value="Save" className="button" />
                                        {canDelete && (
                                            <button onClick={handleDelete} className="button no">Delete user</button>
                                        )}
                                    </li>
                                </ul>
                            </section>
                        )}
                    </div>
                </form>
            </div>

            {/* TODO: Include extra JS */}
        </div>
    );
}
```

שים לב שהקוד הזה הוא רק התחלה. אתה עדיין צריך להוסיף את הפונקציונליות שלך לטיפול בשליחת הטופס ומחיקת המשתמש, ואתה צריך להוסיף את הקומפוננטות שלך לשדות הטופס והכותרת.