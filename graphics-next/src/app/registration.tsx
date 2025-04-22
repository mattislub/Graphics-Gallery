הקובץ שלך משתמש בתבנית Django, אך Next.js משתמש ב-React.js לרינדור של קומפוננטות. לכן, עליך להמיר את הקובץ לקומפוננטת React. הנה דוגמה לקובץ שהומר:

```jsx
import React from 'react';
import Image from 'next/image';
import { useForm } from 'react-hook-form';

export default function Registration() {
  const { register, handleSubmit, errors } = useForm();

  const onSubmit = (data) => {
    // TODO: handle form submission
    console.log(data);
  };

  return (
    <div className="mx-6 mt-12 grow rounded-xl p-5 sm:p-24" style={{ backgroundImage: `url('/media/background_1.webp')` }}>
      <h1 className="text-center font-bold text-xl sm:text-4xl text-white">Registration</h1>
      <div className="relative mx-auto max-w-2xl">
        {/* TODO: Add SVGs and other elements */}
        <div className="mt-4 bg-gradient-2 p-0.5 rounded-3xl">
          <div className="bg-white rounded-3xl px-5 py-2.5 sm:px-10 sm:py-5">
            <div className="flex items-center gap-2.5">
              <div className="h-0.5 bg-blue grow"></div>
              <p className="text-center">To register in {current_site.site_name}</p>
              <div className="h-0.5 bg-blue grow"></div>
            </div>
            <form className="mt-5 rounded-3xl border-2 border-blue p-5" onSubmit={handleSubmit(onSubmit)}>
              <h2 className="text-end font-bold text-xl">Personal Information</h2>
              <input name="name" ref={register({ required: true })} className="mt-5 rounded-full border-2 border-blue w-full text-end" placeholder="Name" />
              {errors.name && <div className="text-xs text-end text-red-500">This field is required</div>}
              <input name="email" ref={register({ required: true })} className="mt-4 rounded-full border-2 border-blue w-full text-end" placeholder="Email" />
              {errors.email && <div className="text-xs text-end text-red-500">This field is required</div>}
              {/* TODO: Add the rest of the form fields */}
              <button type="submit" className="mt-10 mx-auto w-fit flex gap-4 items-center rounded-full font-bold text-lg border-2 border-blue bg-blue text-white py-2 px-5 hover:bg-gradient-2 group">
                <div className="rounded-full border-2 py-0.5 px-5 bg-blue border-white group-hover:border-blue hidden sm:block">
                  {/* TODO: Add SVG */}
                </div>
                Register
              </button>
            </form>
            {/* TODO: Add the rest of the elements */}
          </div>
        </div>
      </div>
    </div>
  );
}
```

שים לב שאני משתמש ב-React Hook Form לניהול הטופס. תצטרך להתקין אותו באמצעות `npm install react-hook-form` או `yarn add react-hook-form`.

כמו כן, אני מניח שיש לך קובץ תמונה בנתיב `/public/media/background_1.webp`. אם התמונה בנתיב אחר, עדכן את הנתיב בהתאם.

לבסוף, עליך להוסיף את הקומפוננטות והאלמנטים שחסרים, כולל ה-SVGs והקישורים.