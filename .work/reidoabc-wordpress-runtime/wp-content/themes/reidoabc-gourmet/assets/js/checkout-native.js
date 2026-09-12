document.addEventListener('DOMContentLoaded', () => {
  const postcode = document.querySelector('#billing_postcode');
  if (!postcode || !window.ReiDoABCCheckout) return;
  postcode.addEventListener('change', async () => {
    const value = postcode.value.replace(/\D/g, '');
    if (value.length !== 8) return;
    try {
      const response = await fetch(`${window.ReiDoABCCheckout.viaCepEndpoint}${value}/json/`);
      const address = await response.json();
      if (address.erro) return;
      const assign = (selector, nextValue) => { const input = document.querySelector(selector); if (input && !input.value) input.value = nextValue || ''; };
      assign('#billing_address_1', address.logradouro);
      assign('#billing_city', address.localidade);
      assign('#billing_state', address.uf);
      document.body.dispatchEvent(new Event('update_checkout'));
    } catch (_) {
      // Address lookup is optional; checkout remains available.
    }
  });
});
