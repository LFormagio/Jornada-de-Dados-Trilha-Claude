# Contract: i18n System

## Module: `i18n.js`

### Purpose
Lightweight internationalization engine that handles locale detection,
string lookup, URL-based locale routing, and dynamic content switching.

### Public API

```javascript
/**
 * Initialize i18n system.
 * - Detects browser locale or reads from localStorage/URL.
 * - Loads the appropriate locale JSON file.
 * - Applies translations to all elements with [data-i18n] attributes.
 *
 * @returns {Promise<void>}
 */
async function init(): Promise<void>

/**
 * Switch the active locale.
 * - Loads new locale file if not cached.
 * - Updates all [data-i18n] elements.
 * - Updates URL prefix.
 * - Stores preference in localStorage.
 * - Emits 'locale-changed' custom event on document.
 *
 * @param {string} locale - 'pt' or 'en'
 * @returns {Promise<void>}
 */
async function setLocale(locale: string): Promise<void>

/**
 * Get a translated string by key.
 * Supports dot-notation keys (e.g., 'nav.about').
 *
 * @param {string} key - Translation key
 * @param {Record<string, string>} [params] - Interpolation params
 * @returns {string} Translated string or key if not found
 */
function t(key: string, params?: Record<string, string>): string

/**
 * Get the current active locale.
 * @returns {string} 'pt' or 'en'
 */
function getLocale(): string
```

### Locale Detection Priority
1. URL path prefix (`/en/...` → `en`, `/pt/...` → `pt`)
2. `localStorage.getItem('preferred-lang')`
3. `navigator.language` (map `pt-BR` → `pt`, `en-*` → `en`)
4. Fallback: `pt`

### Translation Mechanism
- Elements with `data-i18n="key"` have their `textContent` replaced.
- Elements with `data-i18n-placeholder="key"` have their `placeholder` replaced.
- Elements with `data-i18n-aria="key"` have their `aria-label` replaced.
- Dynamic content (from JSON data files) uses `data-i18n-dynamic` and is
  re-rendered by the owning component on locale change.

### URL Routing
- Base URL: `formagio.dev/`
- Locale prefix: `formagio.dev/en/`, `formagio.dev/pt/`
- Hash-based section navigation preserved: `formagio.dev/en/#projects`
- Language switch updates URL without page reload via `history.replaceState`.

### Locale File Structure (UI strings)
```json
{
  "nav": {
    "about": "Sobre",
    "experience": "Experiência",
    "projects": "Projetos",
    "skills": "Skills",
    "certifications": "Certificações",
    "education": "Formação",
    "contact": "Contato"
  },
  "hero": {
    "greeting": "Olá, eu sou",
    "headline": "Analista de Business Intelligence",
    "tagline": "Transformo dados e processos em soluções escaláveis",
    "metric": {
      "years": "anos de experiência",
      "initiatives": "iniciativas gerenciadas",
      "improvements": "melhorias entregues",
      "automations": "automações em produção"
    },
    "cta": {
      "projects": "Ver Projetos",
      "contact": "Entre em Contato"
    },
    "scroll": "Role para baixo"
  }
}
```

### Events
- `locale-changed`: Fired on `document` when locale switches.
  Detail: `{ locale: 'pt' | 'en', previousLocale: 'pt' | 'en' }`
- Components listen for this event to re-render dynamic content.

### Performance
- Locale files are fetched once and cached in memory.
- String lookup is O(1) via pre-built flat key map.
- DOM update uses `querySelectorAll('[data-i18n]')` — fast for ~200 elements.
- Total engine size: < 3KB minified.
