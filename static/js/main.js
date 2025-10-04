// Main JavaScript for MarketingNyt.dk

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuBtn = document.querySelector('.menu-btn');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuBtn && mainNav) {
        menuBtn.addEventListener('click', function() {
            mainNav.classList.toggle('nav-open');
            menuBtn.setAttribute('aria-expanded', 
                menuBtn.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
            );
        });
    }
    
    // Search functionality
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            // Implement search functionality
            console.log('Search clicked');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // FAQ accordion functionality
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const faqItem = this.parentElement;
            const answer = faqItem.querySelector('.faq-answer');
            
            faqItem.classList.toggle('faq-open');
            
            if (faqItem.classList.contains('faq-open')) {
                answer.style.maxHeight = answer.scrollHeight + 'px';
            } else {
                answer.style.maxHeight = '0';
            }
        });
    });
    
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // Share buttons functionality
    document.querySelectorAll('.share-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.href;
            const width = 600;
            const height = 400;
            const left = (window.innerWidth - width) / 2;
            const top = (window.innerHeight - height) / 2;
            
            window.open(url, 'share', 
                `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,resizable=yes`
            );
        });
    });
    
    // Reading progress indicator
    const article = document.querySelector('.article-content');
    if (article) {
        const progressBar = document.createElement('div');
        progressBar.className = 'reading-progress';
        progressBar.innerHTML = '<div class="reading-progress-bar"></div>';
        document.body.appendChild(progressBar);
        
        const progressBarFill = progressBar.querySelector('.reading-progress-bar');
        
        window.addEventListener('scroll', function() {
            const articleTop = article.offsetTop;
            const articleHeight = article.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollTop = window.pageYOffset;
            
            const articleStart = articleTop - windowHeight;
            const articleEnd = articleTop + articleHeight;
            
            if (scrollTop >= articleStart && scrollTop <= articleEnd) {
                const progress = (scrollTop - articleStart) / (articleEnd - articleStart);
                progressBarFill.style.width = Math.min(progress * 100, 100) + '%';
                progressBar.style.opacity = '1';
            } else {
                progressBar.style.opacity = '0';
            }
        });
    }
    
    // Copy link functionality
    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                showNotification('Link kopieret til udklipsholder');
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showNotification('Link kopieret til udklipsholder');
        }
    }
    
    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('notification--show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('notification--show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
                    console.log('DOM content loaded:', perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart, 'ms');
                }
            }, 0);
        });
    }
});

// Add CSS for reading progress and notifications
const style = document.createElement('style');
style.textContent = `
    .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: rgba(0, 0, 0, 0.1);
        z-index: 1000;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .reading-progress-bar {
        height: 100%;
        background-color: #e74c3c;
        width: 0%;
        transition: width 0.1s;
    }
    
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #333;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s;
    }
    
    .notification--show {
        transform: translateX(0);
    }
    
    .notification--info {
        background-color: #2196f3;
    }
    
    .notification--success {
        background-color: #4caf50;
    }
    
    .notification--warning {
        background-color: #ff9800;
    }
    
    .notification--error {
        background-color: #f44336;
    }
    
    @media (max-width: 768px) {
        .nav-open {
            display: block !important;
        }
        
        .main-nav {
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: white;
            border-top: 1px solid #e0e0e0;
            padding: 1rem;
        }
        
        .nav-list {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
`;
document.head.appendChild(style);
