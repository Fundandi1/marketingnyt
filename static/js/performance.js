// Performance optimizations and modern web features
// This file should be loaded with defer attribute

(function() {
    'use strict';

    // Performance monitoring
    const perfObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            if (entry.entryType === 'largest-contentful-paint') {
                console.log('LCP:', entry.startTime);
            }
            if (entry.entryType === 'first-input') {
                console.log('FID:', entry.processingStart - entry.startTime);
            }
            if (entry.entryType === 'layout-shift') {
                if (!entry.hadRecentInput) {
                    console.log('CLS:', entry.value);
                }
            }
        }
    });

    // Observe Core Web Vitals
    try {
        perfObserver.observe({entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift']});
    } catch (e) {
        // Fallback for older browsers
        console.log('Performance Observer not supported');
    }

    // Intersection Observer for lazy loading
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.dataset.src;
                
                if (src) {
                    // Create a new image to preload
                    const newImg = new Image();
                    newImg.onload = () => {
                        img.src = src;
                        img.classList.add('loaded');
                        img.removeAttribute('data-src');
                    };
                    newImg.src = src;
                }
                
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px 0px',
        threshold: 0.01
    });

    // Observe all images with data-src
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });

    // Preload critical resources
    function preloadCriticalResources() {
        const criticalImages = [
            '/static/images/hero-bg.jpg',
            '/media/original_images/logo.png'
        ];

        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }

    // Service Worker registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        });
    }

    // Critical resource hints
    function addResourceHints() {
        const hints = [
            { rel: 'dns-prefetch', href: '//fonts.googleapis.com' },
            { rel: 'dns-prefetch', href: '//www.google-analytics.com' },
            { rel: 'preconnect', href: '//fonts.gstatic.com', crossorigin: true }
        ];

        hints.forEach(hint => {
            const link = document.createElement('link');
            Object.assign(link, hint);
            document.head.appendChild(link);
        });
    }

    // Optimize images based on device capabilities
    function optimizeImages() {
        const images = document.querySelectorAll('img');
        const isHighDPI = window.devicePixelRatio > 1;
        const isSlowConnection = navigator.connection && 
            (navigator.connection.effectiveType === 'slow-2g' || 
             navigator.connection.effectiveType === '2g');

        images.forEach(img => {
            if (isSlowConnection) {
                // Use lower quality images for slow connections
                const src = img.src || img.dataset.src;
                if (src && src.includes('fill-')) {
                    const optimizedSrc = src.replace('fill-', 'fill-').replace('.jpg', '.webp');
                    if (img.dataset.src) {
                        img.dataset.src = optimizedSrc;
                    } else {
                        img.src = optimizedSrc;
                    }
                }
            }
        });
    }

    // Prefetch next page content
    function prefetchNextPage() {
        const links = document.querySelectorAll('a[href^="/"]');
        const prefetchedUrls = new Set();

        const linkObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const link = entry.target;
                    const href = link.href;
                    
                    if (!prefetchedUrls.has(href)) {
                        const prefetchLink = document.createElement('link');
                        prefetchLink.rel = 'prefetch';
                        prefetchLink.href = href;
                        document.head.appendChild(prefetchLink);
                        prefetchedUrls.add(href);
                    }
                }
            });
        }, { threshold: 0.1 });

        links.forEach(link => {
            linkObserver.observe(link);
        });
    }

    // Optimize scroll performance
    let ticking = false;
    function optimizeScroll() {
        function updateScrollPosition() {
            // Batch DOM reads and writes
            const scrollTop = window.pageYOffset;
            const header = document.querySelector('.header');
            
            if (header) {
                if (scrollTop > 100) {
                    header.classList.add('header--scrolled');
                } else {
                    header.classList.remove('header--scrolled');
                }
            }
            
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateScrollPosition);
                ticking = true;
            }
        }, { passive: true });
    }

    // Initialize performance optimizations
    function init() {
        // Run immediately
        addResourceHints();
        optimizeImages();
        optimizeScroll();

        // Run after load
        window.addEventListener('load', () => {
            preloadCriticalResources();
            prefetchNextPage();
        });

        // Run after idle
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                // Non-critical optimizations
                console.log('Running idle optimizations');
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for debugging
    window.MarketingNytPerf = {
        imageObserver,
        preloadCriticalResources,
        optimizeImages
    };

})();
