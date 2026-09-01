// src/i18n/i18n.js
import ptBr from './pt-br.json';
import enUs from './en-us.json';

const locales = {
  'pt': ptBr,
  'en': enUs
};

let currentLocale = 'pt';
let flatTranslations = {};

function flattenObject(ob) {
  var toReturn = {};
  for (var i in ob) {
    if (!ob.hasOwnProperty(i)) continue;
    if ((typeof ob[i]) == 'object' && ob[i] !== null) {
      var flatObject = flattenObject(ob[i]);
      for (var x in flatObject) {
        if (!flatObject.hasOwnProperty(x)) continue;
        toReturn[i + '.' + x] = flatObject[x];
      }
    } else {
      toReturn[i] = ob[i];
    }
  }
  return toReturn;
}

function detectLocale() {
  const pathPrefix = window.location.pathname.split('/')[1];
  if (pathPrefix === 'en' || pathPrefix === 'pt') {
    return pathPrefix;
  }
  
  const stored = localStorage.getItem('preferred-lang');
  if (stored === 'en' || stored === 'pt') return stored;
  
  const browserLang = navigator.language.toLowerCase();
  if (browserLang.startsWith('en')) return 'en';
  
  return 'pt'; // default fallback
}

function updateURL(locale) {
  const path = window.location.pathname;
  let newPath = path;
  
  if (path.startsWith('/en/') || path === '/en') {
    newPath = path.replace(/^\/en/, `/${locale}`);
  } else if (path.startsWith('/pt/') || path === '/pt') {
    newPath = path.replace(/^\/pt/, `/${locale}`);
  } else {
    // No locale prefix, add it (or just use root for default, but let's be explicit)
    if (path === '/') {
       newPath = `/${locale}/`;
    } else {
       newPath = `/${locale}${path}`;
    }
  }
  
  if (newPath !== path) {
    window.history.replaceState({}, '', newPath + window.location.hash);
  }
}

function applyTranslations() {
  document.documentElement.lang = currentLocale === 'pt' ? 'pt-BR' : 'en-US';
  
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (flatTranslations[key]) {
      el.textContent = flatTranslations[key];
    }
  });

  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (flatTranslations[key]) {
      el.setAttribute('placeholder', flatTranslations[key]);
    }
  });

  document.querySelectorAll('[data-i18n-aria]').forEach(el => {
    const key = el.getAttribute('data-i18n-aria');
    if (flatTranslations[key]) {
      el.setAttribute('aria-label', flatTranslations[key]);
    }
  });
}

export async function init() {
  currentLocale = detectLocale();
  flatTranslations = flattenObject(locales[currentLocale]);
  
  updateURL(currentLocale);
  applyTranslations();
}

export async function setLocale(locale) {
  if (locale === currentLocale || !locales[locale]) return;
  
  const previousLocale = currentLocale;
  currentLocale = locale;
  flatTranslations = flattenObject(locales[currentLocale]);
  
  localStorage.setItem('preferred-lang', currentLocale);
  updateURL(currentLocale);
  applyTranslations();
  
  document.dispatchEvent(new CustomEvent('locale-changed', {
    detail: { locale: currentLocale, previousLocale }
  }));
}

export function t(key, params) {
  let str = flatTranslations[key] || key;
  if (params) {
    Object.keys(params).forEach(p => {
      str = str.replace(`{${p}}`, params[p]);
    });
  }
  return str;
}

export function getLocale() {
  return currentLocale;
}
