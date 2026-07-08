// OptiCrop — front-end interactions

document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Animated stat counters ────────────────────────────────────────────
    const counters = document.querySelectorAll('.oc-stat-number[data-target]');
    if (counters.length && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                const el = entry.target;
                const target = parseFloat(el.getAttribute('data-target')) || 0;
                const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
                const duration = 1200;
                const start = performance.now();

                function tick(now) {
                    const p = Math.min((now - start) / duration, 1);
                    const value = target * p;
                    el.textContent = value.toFixed(decimals);
                    if (p < 1) {
                        requestAnimationFrame(tick);
                    } else {
                        el.textContent = target.toFixed(decimals);
                    }
                }
                requestAnimationFrame(tick);
                obs.unobserve(el);
            });
        }, { threshold: 0.4 });
        counters.forEach(function (c) { observer.observe(c); });
    }

    // ── 2. Prediction form validation + submit spinner ───────────────────────
    const form = document.getElementById('predictionForm');
    if (form) {
        const rules = {
            nitrogen:    { min: 0, max: 200, label: 'Nitrogen' },
            phosphorus:  { min: 0, max: 200, label: 'Phosphorus' },
            potassium:   { min: 0, max: 250, label: 'Potassium' },
            temperature: { min: 0, max: 50,  label: 'Temperature' },
            humidity:    { min: 0, max: 100, label: 'Humidity' },
            ph:          { min: 0, max: 14,  label: 'pH' },
            rainfall:    { min: 0, max: 400, label: 'Rainfall' }
        };

        form.addEventListener('submit', function (e) {
            let valid = true;

            Object.keys(rules).forEach(function (name) {
                const field = form.elements[name];
                if (!field) return;
                const rule = rules[name];
                const value = parseFloat(field.value);

                if (field.value.trim() === '' || isNaN(value) || value < rule.min || value > rule.max) {
                    field.classList.add('is-invalid');
                    valid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!valid) {
                e.preventDefault();
                return;
            }

            // Show loading state on the submit button
            const btn = document.getElementById('predictBtn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Analyzing...';
            }
        });

        // Clear the invalid state as the user corrects a field
        form.querySelectorAll('input').forEach(function (input) {
            input.addEventListener('input', function () { input.classList.remove('is-invalid'); });
        });
    }
});
