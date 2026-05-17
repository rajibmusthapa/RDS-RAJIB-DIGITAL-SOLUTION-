// Data statis fallback (jika API mati)
const fallbackProducts = [
    {icon:"💻", name:"Web Development", price:8000000, description:"Website profesional, company profile, marketplace, e-commerce, dan CMS modern."},
    {icon:"📱", name:"Mobile App Development", price:15000000, description:"Aplikasi iOS & Android native dan cross-platform dengan UI/UX modern."},
    {icon:"🔒", name:"Cyber Security", price:10000000, description:"Perlindungan aset digital perusahaan dari ancaman siber."}
];

function toggleMenu() {
    document.getElementById('navLinks')?.classList.toggle('open');
}
function closeMenu() { document.getElementById('navLinks')?.classList.remove('open'); }

async function loadServices() {
    try {
        const res = await fetch('/api/products');
        if(!res.ok) throw new Error('API down');
        const products = await res.json();
        const container = document.getElementById('servicesGrid');
        if(container) container.innerHTML = Object.values(products).map(p => `
            <div class="service-card"><div class="service-icon">${p.icon || '🚀'}</div>
            <h3>${p.name}</h3><p style="font-size:12px;color:#94a3b8">${p.description}</p>
            <div class="service-price">Rp ${p.price.toLocaleString()}</div>
            <a href="#contact" class="btn-card">Konsultasi</a></div>`).join('');
    } catch(e) {
        const container = document.getElementById('servicesGrid');
        if(container) container.innerHTML = fallbackProducts.map(p => `
            <div class="service-card"><div class="service-icon">${p.icon}</div>
            <h3>${p.name}</h3><p style="font-size:12px;color:#94a3b8">${p.description}</p>
            <div class="service-price">Rp ${p.price.toLocaleString()}</div>
            <a href="#contact" class="btn-card">Konsultasi</a></div>`).join('');
    }
}

async function loadPortfolio() {
    try {
        const res = await fetch('/api/portfolio');
        const portfolios = await res.json();
        const container = document.getElementById('portfolioGrid');
        if(portfolios.length === 0) throw new Error('empty');
        container.innerHTML = portfolios.map(p => `<div class="portfolio-card"><div class="service-icon">🚀</div><h3>${p.title}</h3><p style="font-size:12px">${p.category} | ${p.client}</p><a href="#" class="btn-card">Live Demo →</a></div>`).join('');
    } catch(e) {
        document.getElementById('portfolioGrid').innerHTML = '<div style="text-align:center;">Portofolio akan segera hadir</div>';
    }
}

async function loadTestimonials() {
    try {
        const res = await fetch('/api/testimonials');
        const testimonials = await res.json();
        const container = document.getElementById('testimoniGrid');
        if(testimonials.length === 0) throw new Error('empty');
        container.innerHTML = testimonials.map(t => `<div class="testimoni-card"><div class="stars">★★★★★</div><p>"${t.message}"</p><h4>${t.name}</h4><div class="testimoni-reply">💬 RDS: Terima kasih!</div></div>`).join('');
    } catch(e) {
        document.getElementById('testimoniGrid').innerHTML = `
            <div class="testimoni-card"><div class="stars">★★★★★</div><p>"Layanan RDS sangat memuaskan!"</p><h4>Klien Puas</h4><div class="testimoni-reply">💬 RDS: Terima kasih!</div></div>
            <div class="testimoni-card"><div class="stars">★★★★★</div><p>"Profesional dan tepat waktu."</p><h4>Budi Santoso</h4></div>
            <div class="testimoni-card"><div class="stars">★★★★★</div><p>"Support 24/7 sangat membantu."</p><h4>PT Maju Jaya</h4></div>`;
    }
}

// Setup FAQ click handlers
document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('click', () => item.classList.toggle('active'));
});

// Form submission dengan Netlify Forms
const consultForm = document.getElementById('consultationForm');
if(consultForm) {
    consultForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(consultForm);
        const data = Object.fromEntries(formData);
        const resultDiv = document.getElementById('consultResult');
        
        try {
            const res = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(data).toString() });
            if(res.ok) {
                resultDiv.innerHTML = '<span style="color:#10b981">✅ Pesan terkirim! Kami akan segera menghubungi.</span>';
                consultForm.reset();
            } else throw new Error();
        } catch(err) {
            resultDiv.innerHTML = '<span style="color:#ef4444">❌ Gagal mengirim. Silakan coba lagi.</span>';
        }
        setTimeout(() => resultDiv.innerHTML = '', 5000);
    });
}

loadServices(); loadPortfolio(); loadTestimonials();
