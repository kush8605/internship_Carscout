/* ===================================
   WHEELDEAL - homepage.js
   =================================== */

/* ===================================
   SPLASH + REVEAL
   =================================== */
function revealSite() {
  const splash      = document.getElementById('splash');
  const mainContent = document.getElementById('main-content');
  if (!splash || !mainContent) return;

  // Prevent double-run
  if (revealSite._done) return;
  revealSite._done = true;

  setTimeout(() => {
    splash.classList.add('done');
  }, 2000);

  setTimeout(() => {
    splash.style.display = 'none';
    mainContent.classList.add('show');
    initSkeletons();
  }, 2600);
}

// Primary trigger — fires as soon as HTML is parsed, no waiting for images
document.addEventListener('DOMContentLoaded', revealSite);

// Fallback — if script runs after DOMContentLoaded already fired
if (document.readyState !== 'loading') revealSite();


/* ===================================
   NAVBAR JS (unchanged from original)
   =================================== */
(function () {
  const CLOSE_DELAY = 180;
  let closeTimers = new WeakMap();

  function openDropdown(item) {
    clearTimeout(closeTimers.get(item));
    closeTimers.delete(item);
    item.classList.add('open');
  }

  function scheduleClose(item) {
    const t = setTimeout(() => {
      item.classList.remove('open');
      closeTimers.delete(item);
    }, CLOSE_DELAY);
    closeTimers.set(item, t);
  }

  document.querySelectorAll('.nav-item').forEach(item => {
    if (!item.querySelector('.dropdown')) return;
    item.addEventListener('mouseenter', () => openDropdown(item));
    item.addEventListener('mouseleave', () => scheduleClose(item));
    const dd = item.querySelector('.dropdown');
    dd.addEventListener('mouseenter', () => {
      clearTimeout(closeTimers.get(item));
      closeTimers.delete(item);
    });
    dd.addEventListener('mouseleave', () => scheduleClose(item));
  });

  window.setCity = function (e, city) {
    e.preventDefault();
    document.getElementById('city-label').textContent = city;
    document.querySelectorAll('.loc-dropdown .dropdown-item').forEach(el => el.classList.remove('active-city'));
    e.currentTarget.classList.add('active-city');
  };

  const nav = document.getElementById('main-nav');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 10);
  }, { passive: true });

  window.setNavUser = function ({ name, fullName, email }) {
    const initial = name.charAt(0).toUpperCase();
    document.getElementById('nav-avatar').textContent    = initial;
    document.getElementById('nav-avatar-lg').textContent = initial;
    document.getElementById('nav-username').textContent  = name;
    document.getElementById('nav-fullname').textContent  = fullName || name;
    const emailEl = document.querySelector('.user-email');
    if (emailEl && email) emailEl.textContent = email;
    document.getElementById('nav-user-logged').style.display = '';
    document.getElementById('nav-auth-btns').style.display   = 'none';
  };

  window.setNavGuest = function () {
    document.getElementById('nav-user-logged').style.display = 'none';
    document.getElementById('nav-auth-btns').style.display   = '';
  };

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // window.location.href = '/accounts/logout/';
      setNavGuest();
    });
  }

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-item')) {
      document.querySelectorAll('.nav-item.open').forEach(el => el.classList.remove('open'));
    }
  });
})();

/* ===================================
   SEARCH — suggestions dropdown
   =================================== */
const spInput     = document.getElementById('sp-search-input');
const spWrap      = document.getElementById('sp-search-wrap');
const spSugg      = document.getElementById('sp-suggestions');

const allCars = [
  'Hyundai i10','Hyundai i20','Hyundai Creta','Hyundai Venue','Hyundai Eon',
  'Maruti Alto','Maruti Swift','Maruti Baleno','Maruti Wagon R','Maruti Dzire',
  'Maruti Eeco','Maruti Brezza','Maruti Ertiga','Honda City','Honda Amaze',
  'Tata Nexon','Tata Harrier','Tata Punch','Toyota Innova','Toyota Fortuner',
  'Mahindra Scorpio','Mahindra XUV500','Renault Kwid','Ford EcoSport'
];

function openSugg() {
  spSugg.classList.add('open');
  spWrap.classList.add('focused');
}

function closeSugg() {
  spSugg.classList.remove('open');
  spWrap.classList.remove('focused');
}

function renderSuggestions(query) {
  if (!query) {
    // Show trending
    spSugg.innerHTML = `
      <div class="sp-sugg-label">Trending Cars</div>
      <div class="sp-sugg-pills">
        ${['Hyundai i10','Maruti Alto','Maruti Wagon R','Maruti Eeco','Hyundai i20',
           'Maruti Baleno','Maruti Dzire','Hyundai Eon','Honda City','Maruti Swift']
          .map(c => `<span class="sp-sugg-pill" onclick="selectSugg(this)">${c} <i class="fa-solid fa-arrow-trend-up"></i></span>`)
          .join('')}
      </div>`;
  } else {
    const matches = allCars.filter(c => c.toLowerCase().includes(query.toLowerCase())).slice(0, 8);
    if (matches.length === 0) {
      spSugg.innerHTML = `<div class="sp-sugg-label" style="color:#bbb;">No results found</div>`;
    } else {
      spSugg.innerHTML = `
        <div class="sp-sugg-label">Suggestions</div>
        <div class="sp-sugg-pills">
          ${matches.map(c => `<span class="sp-sugg-pill" onclick="selectSugg(this)">${c} <i class="fa-solid fa-magnifying-glass" style="color:#bbb;"></i></span>`).join('')}
        </div>`;
    }
  }
}

if (spInput) {
  spInput.addEventListener('focus', () => { renderSuggestions(''); openSugg(); });
  spInput.addEventListener('input', () => { renderSuggestions(spInput.value); openSugg(); });
  spInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') closeSugg(); });
}

document.addEventListener('click', (e) => {
  if (!e.target.closest('#sp-search-wrap')) closeSugg();
});

window.selectSugg = function(el) {
  const text = el.textContent.trim().replace(/[^\w\s]/g, '').trim();
  if (spInput) spInput.value = text;
  closeSugg();
};

/* ===================================
   SEARCH TABS
   =================================== */
document.querySelectorAll('.sp-tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.sp-tab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

/* ===================================
   DATA
   =================================== */
const categoryData = {
  body: [
    { icon: '🚗', name: 'Hatchback',  count: '12,400+ cars' },
    { icon: '🚙', name: 'SUV',        count: '18,200+ cars' },
    { icon: '🏎️', name: 'Sedan',      count: '9,800+ cars'  },
    { icon: '🚐', name: 'MUV / Van',  count: '3,200+ cars'  },
    { icon: '🛻', name: 'Pickup',     count: '1,400+ cars'  },
    { icon: '💎', name: 'Luxury',     count: '2,100+ cars'  },
  ],
  budget: [
    { icon: '💚', name: 'Under ₹3L',   count: '4,200+ cars'  },
    { icon: '💙', name: '₹3L – ₹5L',   count: '8,600+ cars'  },
    { icon: '💜', name: '₹5L – ₹10L',  count: '14,300+ cars' },
    { icon: '🧡', name: '₹10L – ₹20L', count: '9,800+ cars'  },
    { icon: '❤️', name: 'Above ₹20L',  count: '2,900+ cars'  },
    { icon: '⭐', name: 'Best Deals',  count: '6,700+ cars'  },
  ],
  fuel: [
    { icon: '⛽', name: 'Petrol',   count: '28,400+ cars' },
    { icon: '🛢️', name: 'Diesel',   count: '16,200+ cars' },
    { icon: '⚡', name: 'Electric', count: '3,800+ cars'  },
    { icon: '🌿', name: 'CNG',      count: '4,600+ cars'  },
    { icon: '🔋', name: 'Hybrid',   count: '1,200+ cars'  },
    { icon: '🌱', name: 'LPG',      count: '800+ cars'    },
  ],
};

const carData = [
  { id:1,  name:'Hyundai Creta',      year:2022, variant:'1.5 SX (O) DCT',       km:'28,450 km', fuel:'Petrol',   trans:'Auto',   owners:'1st Owner', price:'₹15.90 L', emi:'EMI ₹28,400/mo', rating:4.8, reviews:124, badge:'CERTIFIED', badgeClass:'',         bodyColor:'#E63946', roofColor:'#c0303b' },
  { id:2,  name:'Maruti Swift',        year:2021, variant:'1.2 ZXI+ AMT',          km:'35,200 km', fuel:'Petrol',   trans:'Auto',   owners:'1st Owner', price:'₹6.80 L',  emi:'EMI ₹12,200/mo', rating:4.6, reviews:89,  badge:'GREAT VALUE', badgeClass:'premium',   bodyColor:'#2563eb', roofColor:'#1d4ed8' },
  { id:3,  name:'Tata Nexon EV',       year:2023, variant:'Max Long Range XZ+',    km:'18,600 km', fuel:'Electric', trans:'Auto',   owners:'1st Owner', price:'₹17.50 L', emi:'EMI ₹31,300/mo', rating:4.9, reviews:67,  badge:'TOP RATED',  badgeClass:'new-lbl',   bodyColor:'#7c3aed', roofColor:'#6d28d9' },
  { id:4,  name:'Honda City',          year:2020, variant:'1.5 V CVT',             km:'52,100 km', fuel:'Petrol',   trans:'Auto',   owners:'2nd Owner', price:'₹11.20 L', emi:'EMI ₹20,000/mo', rating:4.5, reviews:156, badge:'CERTIFIED', badgeClass:'',         bodyColor:'#0891b2', roofColor:'#0e7490' },
  { id:5,  name:'Toyota Innova Crysta',year:2021, variant:'2.4 GX MT 7 Seat',      km:'44,800 km', fuel:'Diesel',   trans:'Manual', owners:'1st Owner', price:'₹19.80 L', emi:'EMI ₹35,400/mo', rating:4.7, reviews:92,  badge:'CERTIFIED', badgeClass:'',         bodyColor:'#065f46', roofColor:'#064e3b' },
  { id:6,  name:'Maruti Baleno',       year:2022, variant:'Alpha CVT',              km:'21,300 km', fuel:'Petrol',   trans:'Auto',   owners:'1st Owner', price:'₹8.45 L',  emi:'EMI ₹15,100/mo', rating:4.6, reviews:78,  badge:'GREAT VALUE', badgeClass:'premium',   bodyColor:'#b45309', roofColor:'#92400e' },
];

/* ===================================
   SVG CAR GENERATOR
   =================================== */
function makeCarSVG(body, roof) {
  return `<svg viewBox="0 0 280 120" width="260" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="140" cy="110" rx="110" ry="7" fill="rgba(0,0,0,0.08)"/>
    <rect x="30" y="72" width="220" height="36" rx="9" fill="${body}"/>
    <path d="M66 72 Q84 44 105 40 L175 40 Q196 44 214 72 Z" fill="${roof}"/>
    <path d="M74 70 Q89 50 106 46 L139 46 L139 70 Z" fill="rgba(255,255,255,0.86)"/>
    <path d="M141 46 L174 46 Q190 50 205 70 L141 70 Z" fill="rgba(255,255,255,0.86)"/>
    <rect x="139" y="46" width="3" height="24" fill="${roof}"/>
    <rect x="32" y="82" width="18" height="10" rx="5" fill="#fef3c7"/>
    <rect x="230" y="82" width="18" height="10" rx="5" fill="#fecaca"/>
    <circle cx="84" cy="109" r="18" fill="#1a1a1a"/>
    <circle cx="84" cy="109" r="11" fill="#2e2e2e"/>
    <circle cx="84" cy="109" r="6" fill="#555"/>
    <circle cx="196" cy="109" r="18" fill="#1a1a1a"/>
    <circle cx="196" cy="109" r="11" fill="#2e2e2e"/>
    <circle cx="196" cy="109" r="6" fill="#555"/>
  </svg>`;
}

/* ===================================
   RENDER FUNCTIONS
   =================================== */
function renderCategories(filter) {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;
  const items = categoryData[filter] || categoryData.body;
  grid.innerHTML = items.map(it => `
    <div class="cat-card fade-in-item">
      <span class="cat-icon">${it.icon}</span>
      <div class="cat-name">${it.name}</div>
      <div class="cat-count">${it.count}</div>
    </div>
  `).join('');
  animateItems(grid.querySelectorAll('.fade-in-item'));
}

function renderCars() {
  const grid = document.getElementById('car-grid');
  if (!grid) return;
  grid.innerHTML = carData.map(car => `
    <div class="car-card fade-in-item" onclick="viewCar(${car.id})">
      <div class="car-img-wrap">
        ${makeCarSVG(car.bodyColor, car.roofColor)}
        <span class="car-badge-lbl ${car.badgeClass}">${car.badge}</span>
        <button class="car-wish" onclick="event.stopPropagation(); toggleWish(this)">🤍</button>
      </div>
      <div class="car-info">
        <div class="car-name">${car.year} ${car.name}</div>
        <div class="car-variant">${car.variant}</div>
        <div class="car-tags">
          <span class="car-tag">📏 ${car.km}</span>
          <span class="car-tag">⛽ ${car.fuel}</span>
          <span class="car-tag">⚙️ ${car.trans}</span>
          <span class="car-tag">👤 ${car.owners}</span>
        </div>
        <div class="car-price-row">
          <div>
            <div class="car-price">${car.price}</div>
            <div class="car-emi">${car.emi}</div>
          </div>
          <div class="car-rating">
            <span class="star">★</span> ${car.rating}
            <small>(${car.reviews})</small>
          </div>
        </div>
      </div>
      <div class="car-cta">
        <button class="btn-view-car" onclick="event.stopPropagation(); viewCar(${car.id})">View Details</button>
        <button class="btn-interest" onclick="event.stopPropagation(); showInterest(${car.id})">I'm Interested →</button>
      </div>
    </div>
  `).join('');
  animateItems(grid.querySelectorAll('.fade-in-item'));
}

function renderWhy() {
  const grid = document.getElementById('why-grid');
  if (!grid) return;
  grid.style.display = '';
  animateItems(grid.querySelectorAll('.why-card'));
}

function renderTestimonials() {
  const grid = document.getElementById('testi-grid');
  if (!grid) return;
  grid.style.display = '';
  animateItems(grid.querySelectorAll('.testi-card'));
}

/* ===================================
   SKELETON → REAL CONTENT
   =================================== */
function swapSkeleton(skeletonId, realId, delay, renderFn) {
  setTimeout(() => {
    const skel = document.getElementById(skeletonId);
    const real = document.getElementById(realId);
    if (!skel || !real) return;
    if (renderFn) renderFn();
    skel.style.transition = 'opacity 0.4s ease';
    skel.style.opacity = '0';
    setTimeout(() => {
      skel.style.display = 'none';
      real.style.display = '';
      real.style.opacity = '0';
      real.style.transition = 'opacity 0.4s ease';
      requestAnimationFrame(() => { real.style.opacity = '1'; });
    }, 400);
  }, delay);
}

function initSkeletons() {
  // Each section reveals with a staggered delay for a natural feel
  swapSkeleton('cat-skeleton',  'cat-grid',   400,  () => renderCategories('body'));
  swapSkeleton('car-skeleton',  'car-grid',   800,  renderCars);
  swapSkeleton('why-skeleton',  'why-grid',   1100, renderWhy);
  swapSkeleton('testi-skeleton','testi-grid', 1400, renderTestimonials);
}

/* ===================================
   SCROLL-TRIGGERED SKELETON LOAD
   (for sections below fold)
   =================================== */
function setupScrollSkeletons() {
  const targets = [
    { trigger: '#sec-why',          skelId: 'why-skeleton',   realId: 'why-grid',    renderFn: renderWhy          },
    { trigger: '#sec-testimonials', skelId: 'testi-skeleton', realId: 'testi-grid',  renderFn: renderTestimonials },
  ];

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const t = targets.find(t => entry.target.matches(t.trigger));
      if (!t) return;
      const skel = document.getElementById(t.skelId);
      const real = document.getElementById(t.realId);
      // Only trigger if still skeleton
      if (!skel || skel.style.display === 'none') return;
      if (t.renderFn) t.renderFn();
      skel.style.transition = 'opacity 0.4s ease';
      skel.style.opacity = '0';
      setTimeout(() => {
        skel.style.display = 'none';
        real.style.display = '';
        real.style.opacity = '0';
        real.style.transition = 'opacity 0.4s ease';
        requestAnimationFrame(() => { real.style.opacity = '1'; });
      }, 400);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15 });

  targets.forEach(t => {
    const el = document.querySelector(t.trigger);
    if (el) observer.observe(el);
  });
}

/* ===================================
   CATEGORY FILTER PILLS
   =================================== */
document.querySelectorAll('.fpill').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.fpill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const grid = document.getElementById('cat-grid');
    if (grid && grid.style.display !== 'none') {
      grid.style.opacity = '0';
      setTimeout(() => {
        renderCategories(btn.dataset.cat);
        grid.style.opacity = '1';
      }, 200);
    }
  });
});

/* ===================================
   FILTER BAR (featured cars)
   =================================== */
document.querySelectorAll('.fbar').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.fbar').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const grid = document.getElementById('car-grid');
    if (grid && grid.style.display !== 'none') {
      grid.style.opacity = '0';
      setTimeout(() => {
        // In production: filter carData by btn.textContent
        renderCars();
        grid.style.opacity = '1';
      }, 200);
    }
  });
});

/* ===================================
   EMI CALCULATOR
   =================================== */
function formatINR(n) {
  return n.toLocaleString('en-IN');
}

function calcEMI() {
  const P = parseInt(document.getElementById('loanAmount')?.value || 500000);
  const r = parseFloat(document.getElementById('interestRate')?.value || 10) / 12 / 100;
  const N = parseInt(document.getElementById('tenure')?.value || 36);
  const emi   = P * r * Math.pow(1+r,N) / (Math.pow(1+r,N)-1);
  const total = emi * N;

  const set = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
  set('loanVal',       formatINR(P));
  set('rateVal',       (r * 12 * 100).toFixed(1).replace('.0',''));
  set('tenureVal',     N);
  set('emiAmount',    `₹${formatINR(Math.round(emi))}`);
  set('principalAmt', `₹${formatINR(P)}`);
  set('totalInterest',`₹${formatINR(Math.round(total-P))}`);
  set('totalAmt',     `₹${formatINR(Math.round(total))}`);
}

['loanAmount','interestRate','tenure'].forEach(id => {
  document.getElementById(id)?.addEventListener('input', calcEMI);
});

calcEMI();

/* ===================================
   INTERACTIONS
   =================================== */
function viewCar(id) {
  showToast(`Opening car #${id} details…`);
  // window.location.href = `/cars/${id}/`;
}

function showInterest(id) {
  showToast('Our team will contact you shortly! 👋');
}

function toggleWish(btn) {
  btn.textContent = btn.textContent === '🤍' ? '❤️' : '🤍';
  showToast(btn.textContent === '❤️' ? 'Added to saved cars ❤️' : 'Removed from saved cars');
}

function showToast(msg) {
  document.querySelector('.wd-toast')?.remove();
  const t = document.createElement('div');
  t.className = 'wd-toast';
  t.textContent = msg;
  t.style.cssText = `
    position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(16px);
    background:#0a0a0a;color:white;padding:12px 24px;border-radius:12px;
    font-family:'Plus Jakarta Sans',sans-serif;font-size:14px;font-weight:600;
    box-shadow:0 8px 32px rgba(0,0,0,.28);z-index:99999;white-space:nowrap;
    opacity:0;transition:all .28s ease;border-left:3px solid #E63946;
  `;
  document.body.appendChild(t);
  requestAnimationFrame(() => {
    t.style.opacity = '1';
    t.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transform = 'translateX(-50%) translateY(8px)';
    setTimeout(() => t.remove(), 300);
  }, 2600);
}

/* ===================================
   FADE-IN ANIMATION HELPER
   =================================== */
function animateItems(items) {
  items.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(18px)';
    el.style.transition = 'opacity .45s ease, transform .45s ease';
    setTimeout(() => {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, i * 80);
  });
}

/* ===================================
   SCROLL REVEAL
   =================================== */
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll('.why-card, .testi-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity .5s ease, transform .5s ease';
    el.classList.add('scroll-reveal');
    observer.observe(el);
  });

  // Add revealed style
  const style = document.createElement('style');
  style.textContent = `.scroll-reveal.revealed { opacity:1 !important; transform:translateY(0) !important; }`;
  document.head.appendChild(style);
}

/* ===================================
   INIT (DOM ready, before splash)
   =================================== */
document.addEventListener('DOMContentLoaded', () => {
  setupScrollSkeletons();
  // Don't call initSkeletons here — called after splash in load event
});