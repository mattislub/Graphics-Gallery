הקובץ שלך משתמש בתבנית Django, אך Next.js משתמש ב-JavaScript ו-React. כאן יש דוגמה של איך הקובץ יכול להיראות ב-Next.js:

```jsx
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';

function SubscriptionPlan() {
  const router = useRouter();
  const [subscriptionPlan, setSubscriptionPlan] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Fetch subscription plan and user data here and set them
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
  };

  if (!subscriptionPlan) {
    return null;
  }

  return (
    <form className="border-blue border-2 rounded-xl h-full p-5 flex gap-5 flex-col md:flex-row text-blue bg-white" method="post" onSubmit={handleSubmit}>
      <input className="" readOnly id="subscription_plan_id" name="subscription_plan_id" type="hidden" value={subscriptionPlan.id} />
      <div className="flex flex-col justify-between order-last md:order-first gap-2.5">
        {user && user.isAuthenticated && (
          <button type="submit" className="mx-auto w-fit flex gap-4 items-center rounded-full font-bold text-lg py-2 px-5 hover:bg-gradient-2 border-2 border-blue" role="link">
            <div className="rounded-full py-0.5 px-5 bg-blue text-white">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
              </svg>
            </div>
            Buy
          </button>
        )}
        {subscriptionPlan.badge_text && (
          <div className="mx-auto w-fit rounded-full font-bold text-lg py-2 px-5 text-white bg-red-500">
            <p>{subscriptionPlan.badge_text}</p>
          </div>
        )}
      </div>
      <div className="flex flex-col gap-2.5 w-full">
        <p className="font-bold text-lg pb-2.5 border-b border-blue text-end">{subscriptionPlan.main_text}</p>
        <p className="font-bold text-lg pb-2.5 border-b border-blue text-end">{subscriptionPlan.help_text}</p>
        <p className="font-bold text-lg pb-2.5 border-b border-blue text-end">{subscriptionPlan.unlimited ? '∞' : subscriptionPlan.download_limit} downloads / {subscriptionPlan.duration_days} days</p>
        <p className="text-lg text-end">Price <span className="text-orange font-bold">₪{subscriptionPlan.price}</span></p>
      </div>
    </form>
  );
}

export default SubscriptionPlan;
```

שים לב שאתה תצטרך להוסיף את הקוד שלך לטעינת המשתמש והתוכנית המנויה מהשרת.