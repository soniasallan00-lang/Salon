document.addEventListener('DOMContentLoaded', () => {

    // 1. Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    // 2. Scroll animations
    const observer = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('aos-animate'); });
    }, { threshold: 0.1 });
    document.querySelectorAll('[data-aos]').forEach(el => observer.observe(el));

    // 3. Mobile nav — hamburger opens drawer, close button / overlay closes it
    const hamburger  = document.getElementById('hamburgerBtn');
    const mobileNav  = document.getElementById('mobileNav');
    const closeNav   = document.querySelector('.close-nav');
    const navOverlay = document.getElementById('mobileNavOverlay');

    function openMobileNav() {
        if (mobileNav) {
            mobileNav.classList.add('open');
            if (navOverlay) navOverlay.classList.add('open');
            document.body.style.overflow = 'hidden';
        }
    }
    function closeMobileNav() {
        if (mobileNav) {
            mobileNav.classList.remove('open');
            if (navOverlay) navOverlay.classList.remove('open');
            document.body.style.overflow = '';
        }
    }

    if (hamburger) hamburger.addEventListener('click', openMobileNav);
    if (closeNav)  closeNav.addEventListener('click', closeMobileNav);
    if (navOverlay) navOverlay.addEventListener('click', closeMobileNav);

    // Close when a link inside mobile nav is clicked
    if (mobileNav) {
        mobileNav.querySelectorAll('a').forEach(function(a) {
            a.addEventListener('click', closeMobileNav);
        });
    }

    // 4. Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const id = this.getAttribute('href');
            if (id === '#') return;
            const target = document.querySelector(id);
            if (target) {
                e.preventDefault();
                window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
            }
        });
    });

});
