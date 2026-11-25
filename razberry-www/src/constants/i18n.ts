/**
 * Updated: 2026-11-25 16:20:00 WIB
 * Deskripsi: Konfigurasi i18n website utama RAZBerry Browser dengan 3 bahasa:
 *            Indo Oke (id-oke sebagai default), Bahasa Indonesia (id), dan English (en).
 */
const UI_ID_OKE = (await import('~/i18n/id-oke/translation.json', { with: { type: 'json' } })).default
const UI_ID = (await import('~/i18n/id/translation.json', { with: { type: 'json' } })).default
const UI_EN = (await import('~/i18n/en/translation.json', { with: { type: 'json' } })).default

export const i18n = {
  // Default bahasa website menggunakan Indo Oke (gaya santai khas RAZ Creative Studio)
  DEFAULT_LOCALE: 'id-oke',
  LOCALES: [
    { label: 'Indo Oke', value: 'id-oke', ui: UI_ID_OKE, intl: 'id-ID' },
    { label: 'Indonesia', value: 'id', ui: UI_ID, intl: 'id-ID' },
    { label: 'English', value: 'en', ui: UI_EN, intl: 'en-US' },
  ],
}

/**
 * Definisi tipe UI translations berdasarkan file terjemahan utama
 */
export type UIProps = typeof UI_ID_OKE | typeof UI_ID | typeof UI_EN

export const getIntlLocale = (locale: string) => {
  return i18n.LOCALES.find(l => l.value === locale)?.intl ?? 'id-ID'
}
