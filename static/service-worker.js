const CACHE_NAME = 'cricket-app-v1';
const FILES_TO_CACHE = [
  '/',
  'manifest.json',
  'icons/10cd9521-c350-429a-bd10-d0e2af47d3ae.png',
  'icons/WhatsApp Ima2.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(FILES_TO_CACHE))
      .catch(err => console.warn('Cache failed:', err))
  );
  self.skipWaiting();
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(resp => resp || fetch(event.request))
  );
});
