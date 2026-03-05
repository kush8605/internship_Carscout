/* =============================================
   WHEELDEAL ADMIN PORTAL — admin.js
   ============================================= */

'use strict';

// =============================================
// CONFIG
// =============================================

const PAGE_TITLES = {
  dashboard:    'Dashboard',
  cars:         'Manage Cars',
  users:        'User Management',
  inquiries:    'Inquiries',
  analytics:    'Analytics',
  transactions: 'Transactions',
  settings:     'Settings'
};

// Simulated load times per page (ms)
const LOAD_TIMES = {
  dashboard:    900,
  cars:         700,
  users:        800,
  inquiries:    600,
  analytics:    1000,
  transactions: 750,
  settings:     500
};

const MONTH_LABELS = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'];

let currentPage = null;
const loadingTimers = {};

// =============================================
// NAVIGATION + SKELETON LOADER
// =============================================

function navigate(page, navEl) {
  // Allow re-navigating to the same page only if it hasn't finished loading yet
  const realEl = document.getElementById('real-' + page);
  const alreadyLoaded = realEl && realEl.style.display !== 'none';
  if (page === currentPage && alreadyLoaded) return;

  currentPage = page;

  // Deactivate all pages + nav items
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  // Activate clicked nav item
  if (navEl) {
    navEl.classList.add('active');
  } else {
    document.querySelectorAll('.nav-item').forEach(n => {
      const text = n.textContent.trim().toLowerCase();
      if (text.includes(page) || text.includes(page.replace(/s$/, ''))) {
        n.classList.add('active');
      }
    });
  }

  // Update topbar title
  const titleEl = document.getElementById('topbar-title');
  if (titleEl) titleEl.textContent = PAGE_TITLES[page] || 'WheelDeal';

  // Show page container
  const pageEl = document.getElementById('page-' + page);
  if (!pageEl) return;
  pageEl.classList.add('active');

  // Show skeleton, hide real content
  const skelEl = document.getElementById('skel-' + page);
  const contentEl = document.getElementById('real-' + page);

  if (skelEl) {
    skelEl.style.display = 'block';
    skelEl.style.opacity = '1';
    skelEl.style.transition = '';
  }
  if (contentEl) {
    contentEl.style.display = 'none';
  }

  // Clear any in-flight timer for this page
  if (loadingTimers[page]) clearTimeout(loadingTimers[page]);

  // After simulated delay, fade out skeleton and reveal real content
  const delay = LOAD_TIMES[page] || 700;

  loadingTimers[page] = setTimeout(() => {
    if (skelEl) {
      skelEl.style.transition = 'opacity 0.25s ease';
      skelEl.style.opacity = '0';
      setTimeout(() => {
        skelEl.style.display = 'none';
        skelEl.style.transition = '';
        revealContent(contentEl);
        afterReveal(page);
      }, 260);
    } else {
      revealContent(contentEl);
      afterReveal(page);
    }
  }, delay);

  if (window.innerWidth <= 900) closeSidebar();
}

function revealContent(realEl) {
  if (!realEl) return;
  realEl.style.display = 'block';
  realEl.classList.add('fade-in');
  setTimeout(() => realEl.classList.remove('fade-in'), 350);
}

function afterReveal(page) {
  if (page === 'dashboard') renderChart('chart',  [82, 95, 110, 128, 98, 145, 132], 'var(--accent)');
  if (page === 'analytics') renderChart('chart2', [31, 42, 38, 55, 48, 62, 58],    '#10b981');
}

// =============================================
// CHART RENDERER
// =============================================

function renderChart(id, data, color) {
  const container = document.getElementById(id);
  if (!container) return;
  const max = Math.max(...data);
  container.innerHTML = data.map((val, i) => {
    const h = (val / max) * 100;
    const o = (0.4 + (val / max) * 0.6).toFixed(2);
    return `<div class="bar" style="background:${color};height:${h}%;opacity:${o}" title="${MONTH_LABELS[i]}: ${val}"><div class="bar-val">${val}</div><div class="bar-lbl">${MONTH_LABELS[i]}</div></div>`;
  }).join('');
}

// =============================================
// MODAL MANAGEMENT
// =============================================

function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('open');
}

function closeModal(id, e) {
  if (!e || e.target === document.getElementById(id)) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('open');
  }
}

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-bg.open').forEach(m => m.classList.remove('open'));
  }
});

// =============================================
// SIDEBAR (MOBILE)
// =============================================

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('open');
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
}

// =============================================
// SETTINGS TABS
// =============================================

function settingsTab(el, tab) {
  document.querySelectorAll('.settings-nav-item').forEach(n => n.classList.remove('active'));
  el.classList.add('active');
  ['profile', 'platform', 'notifications', 'security'].forEach(t => {
    const p = document.getElementById('settings-' + t);
    if (p) p.style.display = t === tab ? 'block' : 'none';
  });
}

// =============================================
// PAGINATION
// =============================================

document.addEventListener('click', e => {
  const btn = e.target.closest('.page-btn');
  if (!btn) return;
  const parent = btn.closest('.pagination');
  if (!parent) return;
  if (!isNaN(btn.textContent.trim())) {
    parent.querySelectorAll('.page-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  }
});

// =============================================
// LOGOUT
// =============================================

function logout() {
  if (confirm('Logout from WheelDeal Admin?')) {
    alert('Redirecting to login...');
  }
}

// =============================================
// INIT
// =============================================

document.addEventListener('DOMContentLoaded', () => {
  // Reset so the guard never blocks the very first load
  currentPage = null;

  // Ensure skeleton is shown and real content is hidden before navigate()
  const dashSkel = document.getElementById('skel-dashboard');
  const dashReal = document.getElementById('real-dashboard');
  if (dashSkel) { dashSkel.style.display = 'block'; dashSkel.style.opacity = '1'; }
  if (dashReal) { dashReal.style.display = 'none'; }

  navigate('dashboard', document.querySelector('.nav-item.active'));
});