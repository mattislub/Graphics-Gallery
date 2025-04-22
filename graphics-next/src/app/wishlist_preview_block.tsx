הקובץ המרוקח:
-----
import { useState } from 'react';
import { useStore } from '../store';
import { useTranslation } from 'next-i18next';

export default function WishlistPreviewBlock() {
    const { t } = useTranslation('common');
    const { wishlist, removeWishlistItem } = useStore();
    const wishlistImages = wishlist.map(item => item.images);

    return (
        <div className="flex flex-col max-h-96 overflow-y-auto z-50">
            {wishlistImages.map((wishlistItem, index) => {
                const [show, setShow] = useState(true);
                const handleRemove = () => {
                    removeWishlistItem(wishlistItem.code);
                    setShow(false);
                };

                return show && (
                    <div key={index} className="flex gap-2.5 sm:gap-5 border-t last:border-b first:border-t-0 border-blue py-2.5">
                        <div className="flex items-start gap-5">
                            <div className="flex flex-col h-full items-center">
                                {wishlistItem.premium ? (
                                    <div className="font-bold bg-green rounded-full flex items-center gap-2 py-1 px-3 eading-none">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                                        </svg>
                                    </div>
                                ) : wishlistItem.subscription_plans.length ? (
                                    <div className="font-bold bg-green rounded-full flex items-center gap-2 py-1 px-3 eading-none">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" className="size-6">
                                            <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0Z" />
                                        </svg>
                                    </div>
                                ) : null}
                                <button className="rounded-full py-0.5 px-2 bg-white bg-opacity-70" onClick={handleRemove}>
                                    <span className="sr-only">{t('Remove from wishlist')}</span>
                                    <div>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="size-6">
                                            <path d="m11.645 20.91-.007-.003-.022-.012a15.247 15.247 0 0 1-.383-.218 25.18 25.18 0 0 1-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0 1 12 5.052 5.5 5.5 0 0 1 16.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 0 1-4.244 3.17 15.247 15.247 0 0 1-.383.219l-.022.012-.007.004-.003.001a.752.752 0 0 1-.704 0l-.003-.001Z" />
                                        </svg>
                                    </div>
                                </button>
                            </div>
                        </div>
                        <div className="ml-auto">
                            <h3 className="leading-tight font-normal tracking-widest text-end">{wishlistItem.name}</h3>
                            <p className="text-xs leading-tight text-end mt-2.5">{wishlistItem.code}</p>
                            {!wishlistItem.subscription_plans.length ? (
                                <p className="my-auto text-base font-bold text-end text-orange">{wishlistItem.price} ₪</p>
                            ) : (
                                <p className="my-auto text-base font-bold text-end text-orange">{t('Free by subscription')}</p>
                            )}
                        </div>
                        <img className="object-fit h-16 self-center rounded-xl" alt={wishlistItem.name} src={wishlistItem.preview_image_url} />
                    </div>
                );
            })}
        </div>
    );
}
-----
אני מניח שיש לך סטור גלובלי שמנהל את הרשימה שלך, אם לא, תצטרך להתאים את הקוד למצב שלך.