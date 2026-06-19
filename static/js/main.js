document.addEventListener('DOMContentLoaded', function() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
        });
    }

    const navbar = document.querySelector('.navbar-algo');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltips.length > 0 && typeof bootstrap !== 'undefined') {
        tooltips.forEach(el => new bootstrap.Tooltip(el));
    }

    const toasts = document.querySelectorAll('.toast');
    if (toasts.length > 0 && typeof bootstrap !== 'undefined') {
        toasts.forEach(el => new bootstrap.Toast(el).show());
    }

    document.querySelectorAll('.alert-dismissible .btn-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.alert').remove();
        });
    });

    const passwordToggles = document.querySelectorAll('.toggle-password');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.closest('.input-group').querySelector('input');
            const icon = this.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('fa-eye', 'fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('fa-eye-slash', 'fa-eye');
            }
        });
    });

    const ctx = document.getElementById('equityChart');
    if (ctx) {
        try {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: JSON.parse(ctx.dataset.labels || '[]'),
                    datasets: [{
                        label: 'Equity',
                        data: JSON.parse(ctx.dataset.values || '[]'),
                        borderColor: '#D4AF37',
                        backgroundColor: 'rgba(212, 175, 55, 0.1)',
                        fill: true,
                        tension: 0.4,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(212,175,55,0.05)' }, ticks: { color: '#64748B' } },
                        y: { grid: { color: 'rgba(212,175,55,0.05)' }, ticks: { color: '#64748B' } }
                    }
                }
            });
        } catch(e) { console.log('Chart not available'); }
    }

    document.querySelectorAll('.newsletter-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            if (!email) return;
            fetch('/newsletter/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: 'email=' + encodeURIComponent(email)
            }).then(r => r.json()).then(d => {
                if (d.status === 'success') {
                    this.querySelector('input[type="email"]').value = '';
                    const btn = this.querySelector('button');
                    const orig = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-check"></i> Subscribed!';
                    setTimeout(() => btn.innerHTML = orig, 3000);
                }
            });
        });
    });

    const notificationBell = document.getElementById('notificationBell');
    if (notificationBell) {
        setInterval(function() {
            fetch('/notifications/count/')
                .then(r => r.json())
                .then(d => {
                    const badge = notificationBell.querySelector('.badge');
                    if (badge) {
                        badge.textContent = d.count;
                        badge.style.display = d.count > 0 ? '' : 'none';
                    }
                });
        }, 30000);
    }
});
