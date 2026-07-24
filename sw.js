// Service Worker básico para habilitar la instalación PWA
const CACHE_NAME = 'acofi-cache-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Filtro de seguridad: Ignorar peticiones de extensiones de Chrome y DevTools
    if (!event.request.url.startsWith('http')) {
        return;
    }
    
    // Para este sistema en vivo, siempre queremos la versión de red más reciente
    event.respondWith(
        fetch(event.request).catch((err) => {
            console.warn('Petición de red interceptada o fallida:', err);
        })
    );
});