document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.getElementById('mainNav');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Close mobile menu if open
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('.navbar-collapse');
                
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
                
                window.scrollTo({
                    top: targetElement.offsetTop - 70,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Portfolio filter
    const filterButtons = document.querySelectorAll('.portfolio-filters button');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            filterButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked button
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            // Show/hide portfolio items based on filter
            portfolioItems.forEach(item => {
                if (filter === 'all' || item.classList.contains(filter)) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    // Before & After Slider
    const beforeAfterSliders = document.querySelectorAll('.before-after-slider');
    
    beforeAfterSliders.forEach(slider => {
        const afterContainer = slider.querySelector('.after-container');
        const sliderHandle = slider.querySelector('.slider-handle');
        let isDown = false;
        
        // Function to update the slider position
        const updateSliderPosition = (clientX) => {
            const rect = slider.getBoundingClientRect();
            const position = (clientX - rect.left) / rect.width;
            const percentage = Math.max(0, Math.min(1, position)) * 100;
            
            afterContainer.style.width = `${percentage}%`;
            sliderHandle.style.left = `${percentage}%`;
        };
        
        // Mouse/Touch events for the slider
        sliderHandle.addEventListener('mousedown', () => {
            isDown = true;
        });
        
        sliderHandle.addEventListener('touchstart', () => {
            isDown = true;
        });
        
        window.addEventListener('mouseup', () => {
            isDown = false;
        });
        
        window.addEventListener('touchend', () => {
            isDown = false;
        });
        
        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            updateSliderPosition(e.clientX);
        });
        
        slider.addEventListener('touchmove', (e) => {
            if (!isDown) return;
            updateSliderPosition(e.touches[0].clientX);
        });
        
        // Allow clicking anywhere on the slider to update position
        slider.addEventListener('click', (e) => {
            updateSliderPosition(e.clientX);
        });
    });
    
    // Add active class to current navigation item based on scroll position
    const sections = document.querySelectorAll('section[id]');
    
    function highlightNavItem() {
        const scrollY = window.pageYOffset;
        
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelector('.nav-link[href="#' + sectionId + '"]')?.classList.add('active');
            } else {
                document.querySelector('.nav-link[href="#' + sectionId + '"]')?.classList.remove('active');
            }
        });
    }
    
    window.addEventListener('scroll', highlightNavItem);
    
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }
    
    // Initialize Lightbox
    if (typeof lightbox !== 'undefined') {
        lightbox.option({
            'resizeDuration': 200,
            'wrapAround': true,
            'fadeDuration': 300,
            'imageFadeDuration': 300,
            'alwaysShowNavOnTouchDevices': true
        });
    }
    
    // Handle form submission with AJAX
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // The form will be handled by Flask form handler
            // No AJAX needed because we're using Flask's form validation
        });
    }
});
