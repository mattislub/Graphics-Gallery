הקובץ המרוקח ב-Next.js יראה כך:

./pages/contact_us.js

התוכן:
-----
import Image from 'next/image'
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

export default function ContactUsPage({ page }) {
    const { t } = useTranslation('common')

    return (
        <div className="container grow mt-12 text-blue">
            <div className="mx-2.5">
                <Image src={page.image} alt="contact-us" className="mx-auto" />
                <h1 className="text-4xl font-black text-center mt-12 leading-9">{page.title}</h1>
                <h2 className="text-3xl font-normal text-center mt-4 leading-8">{page.sub_title}</h2>
                <form className="mt-12 w-full md:w-2/3 mx-auto text-slate-700" id="contact-us-form" action="/api/contact_us" method="post">
                    <div className="mx-2.5 flex flex-col gap-5">
                        <div className="flex gap-5">
                            <input className="w-full rounded-full text-end border-blue" type="email" placeholder={t('Email')} name="email" id="email" />
                            <input className="w-full rounded-full text-end border-blue" type="number" placeholder={t('Phone')} name="phone" id="phone" />
                            <input className="w-full rounded-full text-end border-blue" type="text" placeholder={t('Full name')} name="full_name" id="full_name" />
                        </div>
                        <textarea className="w-full rounded-xl text-end border-blue" name="message" id="message" cols="30" rows="10" placeholder={t('How we can help you?')}></textarea>
                        <button className="self-center w-auto flex gap-4 items-center rounded-full font-bold text-lg border-2 border-blue bg-blue text-white py-2 px-5 hover:bg-gradient-2 group" role="link" type="submit">
                            <div className="rounded-full border-2 py-0.5 px-5 bg-blue border-white group-hover:border-blue">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                                </svg>
                            </div>

                            {t('Send message')}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export async function getServerSideProps({ locale }) {
    return {
        props: {
            ...(await serverSideTranslations(locale, ['common'])),
            // You could also pass some initial props to your component from this function
        },
    }
}
-----

שים לב שהקובץ מניח שיש לך קובץ תרגום בשם 'common' ושאתה משתמש בספריית next-i18next לתרגום. כמו כן, הקובץ מניח שיש לך נתיב API בשם '/api/contact_us' שמטפל בשליחת הטופס.