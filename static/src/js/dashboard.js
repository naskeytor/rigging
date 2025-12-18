/** @odoo-module **/

const EXPANDED = "rg-is-expanded";
const LOCK_SCROLL = "rg-dashboard-lock-scroll";
const OVERLAY_CLASS = "rg_dashboard_overlay";

let active = null; // { card, placeholder }

function closest(el, sel) {
  return el ? el.closest(sel) : null;
}

function ensureOverlay() {
  let overlay = document.querySelector(`.${OVERLAY_CLASS}`);
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.className = OVERLAY_CLASS;
    overlay.addEventListener("click", minimizeAll, true);
    document.body.appendChild(overlay);
  }
}

function removeOverlay() {
  const overlay = document.querySelector(`.${OVERLAY_CLASS}`);
  if (overlay) overlay.remove();
}

function expandCard(card) {
  minimizeAll();

  const placeholder = document.createElement("div");
  placeholder.className = "rg_placeholder";
  card.parentNode.insertBefore(placeholder, card);

  // Portal a body (evita overflow/transform de Odoo)
  document.body.appendChild(card);

  card.classList.add(EXPANDED);
  document.documentElement.classList.add(LOCK_SCROLL);
  document.body.classList.add(LOCK_SCROLL);

  ensureOverlay();
  active = { card, placeholder };
}

function minimizeAll() {
  if (!active) return;

  const { card, placeholder } = active;

  card.classList.remove(EXPANDED);

  if (placeholder && placeholder.parentNode) {
    placeholder.parentNode.insertBefore(card, placeholder);
    placeholder.remove();
  }

  active = null;

  document.documentElement.classList.remove(LOCK_SCROLL);
  document.body.classList.remove(LOCK_SCROLL);
  removeOverlay();
}

/**
 * 🔥 CAPTURE handler:
 * Se ejecuta antes de que Odoo intercepte el click del <button>.
 */
function clickHandler(ev) {
  const expandBtn = closest(ev.target, ".rg_expand_btn");
  if (expandBtn) {
    const card = closest(expandBtn, ".rg_dashboard_card");
    if (card) expandCard(card);
    ev.preventDefault();
    ev.stopPropagation();
    return;
  }

  const minimizeBtn = closest(ev.target, ".rg_minimize_btn");
  if (minimizeBtn) {
    minimizeAll();
    ev.preventDefault();
    ev.stopPropagation();
    return;
  }
}

// Listener en CAPTURE phase (true)
document.addEventListener("click", clickHandler, true);

document.addEventListener("keydown", (ev) => {
  if (ev.key === "Escape") minimizeAll();
}, true);