if (typeof tailwind !== 'undefined') {
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: { 300:'#93c5fd', 400:'#60a5fa', 500:'#3b82f6', 600:'#2563eb', 700:'#1d4ed8' },
          accent:  { 400:'#22d3ee', 500:'#06b6d4' },
          dark:    { 900:'#080c14', 800:'#0f1828', 700:'#1e2d4a', 600:'#263352' }
        },
        fontFamily: { syne: ['Syne','sans-serif'], dm: ['DM Sans','sans-serif'] }
      }
    }
  }
}

function toggleMenu() {
  const m = document.getElementById('mobile-menu');
  if (m) m.classList.toggle('hidden');
}

const Toast = {
  container: null,
  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'fixed bottom-5 right-5 z-[9999] flex flex-col gap-3';
      document.body.appendChild(this.container);
    }
  },
  show(msg, type='success') {
    this.init();
    const t = document.createElement('div');
    const cfg = {
      success: { bg:'bg-green-500/15 border-green-500', icon:'fa-check-circle text-green-400' },
      error:   { bg:'bg-red-500/15 border-red-500',     icon:'fa-times-circle text-red-400' },
      info:    { bg:'bg-primary-500/15 border-primary-500', icon:'fa-info-circle text-primary-400' },
    };
    const { bg, icon } = cfg[type] || cfg.info;
    t.className = `glass flex items-center gap-3 px-4 py-3 rounded-xl border-l-4 shadow-xl min-w-[260px] max-w-[360px] toast-enter ${bg}`;
    t.innerHTML = `<i class="fas ${icon} text-xl flex-shrink-0"></i><p class="text-white text-sm font-medium flex-1">${msg}</p><button onclick="this.parentElement.remove()" class="text-gray-400 hover:text-white ml-1"><i class="fas fa-times text-xs"></i></button>`;
    this.container.appendChild(t);
    setTimeout(() => { if(t.parentElement){ t.classList.replace('toast-enter','toast-exit'); setTimeout(()=>t.remove(),310); } }, 3200);
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const yr = document.getElementById('current-year');
  if (yr) yr.textContent = new Date().getFullYear();

  // Show Django messages as toasts
  document.querySelectorAll('.django-message').forEach(el => {
    Toast.show(el.dataset.text, el.dataset.type || 'info');
  });
});
