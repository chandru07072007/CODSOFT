// static/js/main.js

console.log('main.js loaded ✅');

// ========== CART FUNCTIONS ==========

// Confirm before adding item to cart
function confirmAddToCart(productName) {
    return confirm(`Add "${productName}" to your cart?`);
}

// Update cart count dynamically
function updateCartCount(count) {
    const cartLink = document.querySelector('a[href$="view_cart"]');
    if (cartLink) {
        cartLink.textContent = `Cart (${count})`;
    }
}

// Show a temporary notification (toast)
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 50);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ========== SEARCH & FILTER ==========

// Instant search filter
function setupInstantSearch() {
    const searchInput = document.querySelector('.search-form input[name="q"]');
    const productCards = document.querySelectorAll('.product-card');

    if (!searchInput || productCards.length === 0) return;

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        let found = false;
        productCards.forEach(card => {
            const title = card.querySelector('.product-title').textContent.toLowerCase();
            if (title.includes(query)) {
                card.style.display = 'block';
                found = true;
            } else {
                card.style.display = 'none';
            }
        });
        if (!found) {
            showToast('No matching products found', 'error');
        }
    });
}

// Price range filter
function setupPriceFilter() {
    const rangeInput = document.querySelector('#priceRange');
    const priceValue = document.querySelector('#priceValue');
    const productCards = document.querySelectorAll('.product-card');

    if (!rangeInput || productCards.length === 0) return;

    rangeInput.addEventListener('input', function () {
        priceValue.textContent = `₹${this.value}`;
        productCards.forEach(card => {
            const price = parseFloat(card.dataset.price);
            card.style.display = price <= this.value ? 'block' : 'none';
        });
    });
}

// ========== UI ENHANCEMENTS ==========

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Highlight active navigation link
function highlightActiveNav() {
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active-link');
        }
    });
}

// Dark mode toggle
function setupDarkMode() {
    const toggle = document.querySelector('#darkModeToggle');
    if (!toggle) return;

    toggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
    });

    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// Image zoom on hover
function setupImageZoom() {
    const images = document.querySelectorAll('.product-card img');
    images.forEach(img => {
        img.addEventListener('mouseenter', () => {
            img.style.transform = 'scale(1.1)';
        });
        img.addEventListener('mouseleave', () => {
            img.style.transform = 'scale(1)';
        });
    });
}

// Run functions after DOM loads
document.addEventListener('DOMContentLoaded', () => {
    setupInstantSearch();
    setupPriceFilter();
    highlightActiveNav();
    setupDarkMode();
    setupImageZoom();
});
