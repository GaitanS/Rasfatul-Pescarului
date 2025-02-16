// Navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const navbarHeight = navbar.offsetHeight;
    const navbarBrand = document.querySelector('.navbar-brand');
    
    function handleScroll() {
        if (window.scrollY > navbarHeight) {
            navbar.classList.add('scrolled');
            navbarBrand.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
            navbarBrand.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll);
});

// Smooth scroll for anchor links
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

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Handle mobile menu
document.addEventListener('DOMContentLoaded', function() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        // Initialize Bootstrap collapse
        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
            toggle: false
        });

        // Initialize all dropdowns
        const dropdowns = document.querySelectorAll('.dropdown-toggle');
        dropdowns.forEach(dropdown => {
            new bootstrap.Dropdown(dropdown, {
                popperConfig: function (defaultBsPopperConfig) {
                    return defaultBsPopperConfig;
                }
            });
        });

        // Toggle menu when button is clicked
        navbarToggler.addEventListener('click', function() {
            bsCollapse.toggle();
        });

        // Handle mobile dropdown clicks
        if (window.innerWidth <= 768) {
            document.querySelectorAll('.dropdown-toggle').forEach(function(element) {
                element.addEventListener('click', function(e) {
                    if (window.innerWidth <= 768) {
                        // If we're on mobile, follow the link directly
                        window.location.href = this.getAttribute('href');
                        return;
                    }
                    // On desktop, keep default dropdown behavior
                    e.preventDefault();
                    e.stopPropagation();
                    const dropdownMenu = this.nextElementSibling;
                    if (dropdownMenu) {
                        // Close other dropdowns
                        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                            if (menu !== dropdownMenu) {
                                menu.classList.remove('show');
                            }
                        });
                        dropdownMenu.classList.toggle('show');
                    }
                });
            });

            // Close dropdown when clicking its items
            document.querySelectorAll('.dropdown-item').forEach(item => {
                item.addEventListener('click', () => {
                    bsCollapse.hide();
                    document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                        menu.classList.remove('show');
                    });
                });
            });
        }

        // Close menu when clicking a regular link
        document.querySelectorAll('.navbar-nav .nav-link:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                bsCollapse.hide();
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navbarCollapse.contains(e.target) && 
                !navbarToggler.contains(e.target) && 
                navbarCollapse.classList.contains('show')) {
                bsCollapse.hide();
                // Also close any open dropdowns
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    }
});

// Lazy loading for images
document.addEventListener('DOMContentLoaded', function() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Auto-hide alerts after 3 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 3000);
});
