// Evita dobles envíos accidentales en formularios de autenticación.
document.querySelectorAll('form[method="post"]').forEach((form) => {
  form.addEventListener("submit", () => {
    const button = form.querySelector('button[type="submit"]');
    if (button) { button.disabled = true; button.textContent = "Procesando…"; }
  });
});
