// Tailwind Config
if(typeof tailwind !== 'undefined') {
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: { 400: '#fb923c', 500: '#f97316', 600: '#ea580c' },
          dark:    { 900: '#0f172a', 800: '#1e293b', 700: '#334155' }
        },
        fontFamily: { outfit: ['Outfit', 'sans-serif'] }
      }
    }
  }
}

function toggleMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) menu.classList.toggle('hidden');
}

const Toast = {
  container: null,
  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-3 font-outfit';
      document.body.appendChild(this.container);
    }
  },
  show(message, type = 'success') {
    this.init();
    const toast = document.createElement('div');
    const bgClass   = type==='success' ? 'bg-green-500/20 border-green-500' : type==='error' ? 'bg-red-500/20 border-red-500' : 'bg-primary-500/20 border-primary-500';
    const iconClass = type==='success' ? 'fa-check-circle text-green-400'   : type==='error' ? 'fa-times-circle text-red-400'   : 'fa-info-circle text-primary-500';
    toast.className = `glass flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 shadow-lg min-w-[250px] max-w-[350px] toast-enter ${bgClass}`;
    toast.innerHTML = `<i class="fas ${iconClass} text-xl"></i><p class="text-white text-sm font-medium flex-1">${message}</p><button onclick="this.parentElement.style.display='none'" class="text-gray-400 hover:text-white transition"><i class="fas fa-times"></i></button>`;
    this.container.appendChild(toast);
    setTimeout(() => {
      if(toast.parentElement) {
        toast.classList.replace('toast-enter','toast-exit');
        setTimeout(() => toast.remove(), 300);
      }
    }, 3500);
  }
};

function animateSkillBars() {
  document.querySelectorAll('.skill-bar-fill').forEach(bar => {
    bar.style.width = bar.getAttribute('data-width') + '%';
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const yearSpan = document.getElementById('current-year');
  if(yearSpan) yearSpan.textContent = new Date().getFullYear();

  // Skill bars IntersectionObserver
  const skillsSection = document.getElementById('skills');
  if(skillsSection) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => { if(e.isIntersecting) { animateSkillBars(); obs.unobserve(e.target); } });
    }, { threshold: 0.3 });
    obs.observe(skillsSection);
  }
});
