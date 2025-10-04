// Service Worker for MarketingNyt.dk
// Provides caching, offline functionality, and performance optimizations

const CACHE_NAME = 'marketingnyt-v1.0.0';
const STATIC_CACHE = 'marketingnyt-static-v1.0.0';
const DYNAMIC_CACHE = 'marketingnyt-dynamic-v1.0.0';

// Resources to cache immediately
const STATIC_ASSETS = [
    '/',
    '/static/css/critical.css',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/js/performance.js',
    '/static/images/favicon.ico',
    '/offline.html'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
                            console.log('Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache with network fallback
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip admin and API requests
    if (url.pathname.startsWith('/admin/') || 
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/django-admin/')) {
        return;
    }

    event.respondWith(
        caches.match(request)
            .then(cachedResponse => {
                if (cachedResponse) {
                    // Serve from cache
                    return cachedResponse;
                }

                // Network request with caching
                return fetch(request)
                    .then(response => {
                        // Don't cache error responses
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone response for caching
                        const responseToCache = response.clone();

                        // Determine cache strategy based on resource type
                        let cacheName = DYNAMIC_CACHE;
                        
                        if (isStaticAsset(url)) {
                            cacheName = STATIC_CACHE;
                        }

                        // Cache the response
                        caches.open(cacheName)
                            .then(cache => {
                                cache.put(request, responseToCache);
                            });

                        return response;
                    })
                    .catch(() => {
                        // Offline fallback
                        if (request.destination === 'document') {
                            return caches.match('/offline.html');
                        }
                        
                        // Return placeholder for images
                        if (request.destination === 'image') {
                            return new Response(
                                '<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#f0f0f0"/><text x="50%" y="50%" text-anchor="middle" dy=".3em" fill="#999">Billede ikke tilgængeligt</text></svg>',
                                { headers: { 'Content-Type': 'image/svg+xml' } }
                            );
                        }
                    });
            })
    );
});

// Background sync for form submissions
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Push notifications
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/images/icon-192x192.png',
            badge: '/static/images/badge-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: data.primaryKey
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Læs artikel',
                    icon: '/static/images/checkmark.png'
                },
                {
                    action: 'close',
                    title: 'Luk',
                    icon: '/static/images/xmark.png'
                }
            ]
        };

        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Notification click handling
self.addEventListener('notificationclick', event => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Helper functions
function isStaticAsset(url) {
    return url.pathname.startsWith('/static/') ||
           url.pathname.endsWith('.css') ||
           url.pathname.endsWith('.js') ||
           url.pathname.endsWith('.png') ||
           url.pathname.endsWith('.jpg') ||
           url.pathname.endsWith('.jpeg') ||
           url.pathname.endsWith('.gif') ||
           url.pathname.endsWith('.svg') ||
           url.pathname.endsWith('.webp');
}

function doBackgroundSync() {
    // Handle background sync for offline form submissions
    return new Promise((resolve) => {
        // Implementation for syncing offline data
        console.log('Background sync completed');
        resolve();
    });
}

// Cache management
function cleanupCache() {
    return caches.open(DYNAMIC_CACHE)
        .then(cache => {
            return cache.keys()
                .then(requests => {
                    if (requests.length > 50) {
                        // Remove oldest entries
                        return cache.delete(requests[0]);
                    }
                });
        });
}

// Periodic cleanup
setInterval(cleanupCache, 60000); // Every minute
