/* ============================================================
   VELARÉ ESCAPE — script.js (Producción con Render)
============================================================ */

/* ——— NAVBAR: scroll effect + hamburger ——— */
const navbar    = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
const navCta    = document.querySelector('.navbar__cta');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
});

hamburger.addEventListener('click', () => {
  const isOpen = hamburger.classList.toggle('open');
  navLinks.classList.toggle('open', isOpen);
  if (navCta) navCta.classList.toggle('open', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
  hamburger.setAttribute('aria-expanded', isOpen);
});

// Close menu when a link is clicked
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinks.classList.remove('open');
    if (navCta) navCta.classList.remove('open');
    document.body.style.overflow = '';
  });
});


/* ——— PACKAGE FILTER ——— */
const filterBtns = document.querySelectorAll('.filter-btn');
const pkgCards   = document.querySelectorAll('.pkg-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.filter;

    pkgCards.forEach(card => {
      if (filter === 'todos' || card.dataset.category === filter) {
        card.hidden = false;
      } else {
        card.hidden = true;
      }
    });
  });
});


/* ——— FORM VALIDATION & SUBMISSION ——— */
const form       = document.getElementById('contactForm');
const submitBtn  = document.getElementById('submitBtn');
const btnText    = submitBtn.querySelector('.btn-text');
const btnLoading = submitBtn.querySelector('.btn-loading');
const formSuccess = document.getElementById('formSuccess');

const fields = {
  nombre:     { el: document.getElementById('nombre'),    err: document.getElementById('errorNombre') },
  correo:     { el: document.getElementById('correo'),    err: document.getElementById('errorCorreo') },
  asunto:     { el: document.getElementById('asunto'),    err: document.getElementById('errorAsunto') },
  mensaje:    { el: document.getElementById('mensaje'),   err: document.getElementById('errorMensaje') },
  privacidad:{ el: document.getElementById('privacidad'),err: document.getElementById('errorPrivacidad') },
};

function validateField(name) {
  const { el, err } = fields[name];
  let msg = '';

  if (name === 'privacidad') {
    if (!el.checked) msg = 'Debes aceptar el aviso de privacidad.';
  } else if (!el.value.trim()) {
    msg = 'Este campo es requerido.';
  } else if (name === 'correo') {
    const emailRx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRx.test(el.value.trim())) msg = 'Ingresa un correo electrónico válido.';
  } else if (name === 'nombre' && el.value.trim().length < 2) {
    msg = 'Ingresa al menos 2 caracteres.';
  } else if (name === 'mensaje' && el.value.trim().length < 10) {
    msg = 'El mensaje debe tener al menos 10 caracteres.';
  }

  err.textContent = msg;
  el.classList.toggle('error', msg !== '');
  return msg === '';
}

// Live validation on blur
Object.keys(fields).forEach(name => {
  const { el } = fields[name];
  el.addEventListener('blur', () => validateField(name));
  el.addEventListener('input', () => {
    if (el.classList.contains('error')) validateField(name);
  });
});