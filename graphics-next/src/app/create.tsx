ב-Next.js, נשתמש בקומפוננטות React במקום תבניות Django. קובץ ה-JSX המומר יראה כך:

```jsx
import { useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';

import Header from '../components/Header';
import Field from '../components/Field';
import TabNavLink from '../components/TabNavLink';

export default function CreateUser() {
  const { t } = useTranslation('users');
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState('account');

  const onSubmit = async (data) => {
    // TODO: Implement form submission
  };

  return (
    <div>
      <Header title={t('createUser')} icon="user" merged={1} />

      <div className="w-tabs" data-tabs>
        <div className="w-tabs__wrapper">
          <div role="tablist" className="w-tabs__list">
            <TabNavLink tabId='account' title={t('account')} />
            <TabNavLink tabId='roles' title={t('roles')} />
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="tab-content">
            <section id="tab-account" className="w-tabs__panel" role="tabpanel" hidden={activeTab !== 'account'}>
              <ul className="fields">
                <Field register={register} errors={errors} name="username" />
                <Field register={register} errors={errors} name="email" />
                <Field register={register} errors={errors} name="first_name" />
                <Field register={register} errors={errors} name="last_name" />
                <Field register={register} errors={errors} name="balance" />

                <Field register={register} errors={errors} name="is_active" />
                <Field register={register} errors={errors} name="registration_date" />

                <Field register={register} errors={errors} name="balance_replenishment_notification" />
                <Field register={register} errors={errors} name="purchase_notification" />
                <Field register={register} errors={errors} name="filled_cart_notification" />

                <Field register={register} errors={errors} name="password1" />
                <Field register={register} errors={errors} name="password2" />

                <li>
                  <button onClick={() => setActiveTab('roles')} className="button">
                    {t('roles')}
                  </button>
                </li>
              </ul>
            </section>

            <section id="tab-roles" className="w-tabs__panel" role="tabpanel" hidden={activeTab !== 'roles'}>
              <ul className="fields">
                <Field register={register} errors={errors} name="is_superuser" />
                <li><button type="submit" className="button">{t('addUser')}</button></li>
              </ul>
            </section>
          </div>
        </form>
      </div>
    </div>
  );
}

export async function getServerSideProps({ locale }) {
  return {
    props: {
      ...await serverSideTranslations(locale, ['users']),
    },
  };
}
```

הערה: זה הוא רק דוגמה כיצד להמיר את הקוד, ויתכן שתצטרך להתאים את הקוד לפי הצרכים שלך. לדוגמה, תצטרך להוסיף קוד לשליחת הטופס ולהציג שגיאות. כמו כן, תצטרך ליצור את הקומפוננטות `Header`, `Field` ו-`TabNavLink`.