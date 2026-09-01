// src/components/contact/contact.js
import { getLocale } from '../../i18n/i18n.js';

export function initContact() {
  const btnDownloadCv = document.getElementById('btn-download-cv');
  if (!btnDownloadCv) return;

  btnDownloadCv.addEventListener('click', () => {
    const locale = getLocale();
    const filename = locale === 'pt' ? 'CV PT.BR (ATS) - Lucas Formagio.pdf' : 'CV EN.US (ATS) - Lucas Formagio.pdf';
    
    // Create an invisible link to trigger download
    const link = document.createElement('a');
    link.href = `/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
}
