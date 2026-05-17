// ============ DATA STATIS (TANPA BACKEND) ============
const PRODUCTS = {
    "1": {"id": "1", "name": "💻 Web Development", "price": "Rp 8.000.000 - 75.000.000", "description": "Website profesional, company profile, marketplace, e-commerce, dan CMS modern."},
    "2": {"id": "2", "name": "📱 Mobile App Development", "price": "Rp 15.000.000 - 150.000.000", "description": "Aplikasi iOS & Android native dan cross-platform dengan UI/UX modern."},
    "3": {"id": "3", "name": "🔒 Cyber Security", "price": "Rp 10.000.000 - 85.000.000", "description": "Perlindungan aset digital perusahaan dari ancaman siber."}
};

const PORTFOLIOS = [
    {"title": "E-Commerce Marketplace", "category": "Website", "client": "PT. Maju Jaya", "desc": "Full Stack Web App dengan payment gateway"},
    {"title": "Company Profile Digital", "category": "Website", "client": "CV. Kreatif", "desc": "Sistem manajemen proyek rating A+ security"},
    {"title": "Laundry Mobile App", "category": "Mobile App", "client": "Laundry Cepat", "desc": "Aplikasi pesan antar laundry dengan tracking"}
];

const TESTIMONIALS = [
    {"name": "Donwahab Pool", "message": "Kami kasih rating 6/6 untuk layanan RDS. Website yang dibuat simpel, rapi, dan mudah diakses lewat HP.", "rating": 5},
    {"name": "Enjang Rahman", "message": "Sangat bagus 👍", "rating": 5},
    {"name": "Mio Soul", "message": "Mantap trimakasi ❤️", "rating": 5}
];

// Simpan booking di localStorage (tetap ada meskipun refresh)
let bookings = JSON.parse(localStorage.getItem('rds_bookings') || '[]');

// Load Services
function loadServices() {
    const container = document.getElementById('servicesGrid');
    if (container) {
        container.innerHTML = Object.values(PRODUCTS).map(p => `
            <div class="service-card">
                <div class="service-icon">${p.name.split(' ')[0]}</div>
                <h3>${p.name}</h3>
                <p>${p.description}</p>
                <div class="service-price">${p.price}</div>
                <a href="#contact" class="btn-card">Konsultasi</a>
            </div>
        `).join('');
    }
}

// Load Portfolio
function loadPortfolio() {
    const container = document.getElementById('portfolioGrid');
    if (container) {
        container.innerHTML = PORTFOLIOS.map(p => `
            <div class="portfolio-card">
                <div class="service-icon">🚀</div>
                <h3>${p.title}</h3>
                <p>${p.category} | ${p.client}</p>
                <p style="font-size:12px;color:#94a3b8">${p.desc}</p>
                <a href="#" class="btn-card">Live Demo →</a>
            </div>
        `).join('');
    }
}

// Load Testimonials
function loadTestimonials() {
    const container = document.getElementById('testimoniGrid');
    if (container) {
        container.innerHTML = TESTIMONIALS.map(t => `
            <div class="testimoni-card">
                <div class="stars">${'★'.repeat(t.rating)}</div>
                <p>"${t.message}"</p>
                <h4>${t.name}</h4>
                <div class="testimoni-reply">💬 RDS: Terima kasih!</div>
            </div>
        `).join('');
    }
}

// Submit Booking (simpan ke localStorage)
const consultForm = document.getElementById('consultationForm');
if (consultForm) {
    consultForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(consultForm);
        const booking = {
            id: bookings.length + 1,
            name: formData.get('fullName'),
            email: formData.get('email'),
            service: formData.get('service'),
            message: formData.get('message'),
            date: new Date().toISOString(),
            status: 'pending'
        };
        
        bookings.push(booking);
        localStorage.setItem('rds_bookings', JSON.stringify(bookings));
        
        const resultDiv = document.getElementById('consultResult');
        resultDiv.innerHTML = '<span style="color:#10b981">✅ Booking terkirim! Admin akan segera menghubungi.</span>';
        consultForm.reset();
        setTimeout(() => resultDiv.innerHTML = '', 5000);
    });
}

// Toggle menu
function toggleMenu() { document.getElementById('navLinks')?.classList.toggle('open'); }
function closeMenu() { document.getElementById('navLinks')?.classList.remove('open'); }

// Load all
loadServices();
loadPortfolio();
loadTestimonials();

// ============ SUPABASE CONFIG ============
const SUPABASE_URL = 'https://rxavqieahctcoumxdsuy.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_Om2bBc8abrILDagNByy2ZQ_qhyrVntD';

