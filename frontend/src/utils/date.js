/**
 * Formats a UTC date string to a local time string.
 * @param {string} dateStr - The date string from the backend.
 * @param {Object} options - Intl.DateTimeFormat options.
 * @returns {string} Formatted local date string.
 */
export function formatToLocalTime(dateStr, options = { dateStyle: 'medium', timeStyle: 'short' }) {
  if (!dateStr) return 'Fecha no disponible';

  // Normalize: replace space with 'T' and ensure it ends with 'Z' to force UTC interpretation
  const normalizedDate = dateStr.replace(' ', 'T');
  const utcDateStr = normalizedDate.endsWith('Z') ? normalizedDate : `${normalizedDate}Z`;
  
  const date = new Date(utcDateStr);

  if (isNaN(date.getTime())) {
    return 'Fecha inválida';
  }

  return date.toLocaleString('es-CO', options);
}

/**
 * Checks if a UTC date string corresponds to the current local day.
 * @param {string} dateStr - The UTC date string from the backend.
 * @returns {boolean} True if it's today local time.
 */
export function isSameDayLocal(dateStr) {
  if (!dateStr) return false;
  
  const normalizedDate = dateStr.replace(' ', 'T');
  const utcDateStr = normalizedDate.endsWith('Z') ? normalizedDate : `${normalizedDate}Z`;
  const matchDate = new Date(utcDateStr);
  const today = new Date();
  
  if (isNaN(matchDate.getTime())) return false;
  
  return (
    matchDate.getFullYear() === today.getFullYear() &&
    matchDate.getMonth() === today.getMonth() &&
    matchDate.getDate() === today.getDate()
  );
}

/**
 * Formats a UTC date string to the YYYY-MM-DDTHH:mm format required by datetime-local inputs,
 * adjusted to the user's local timezone.
 * @param {string} dateStr - The UTC date string from the backend.
 * @returns {string} The formatted local date string.
 */
export function formatToDateTimeLocal(dateStr) {
  if (!dateStr) return '';

  const normalizedDate = dateStr.replace(' ', 'T');
  const utcDateStr = normalizedDate.endsWith('Z') ? normalizedDate : `${normalizedDate}Z`;
  const date = new Date(utcDateStr);

  if (isNaN(date.getTime())) return '';

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${year}-${month}-${day}T${hours}:${minutes}`;
}
