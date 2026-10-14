<!-- Package: 00_skills/(quality)/web-accessibility; relative command/resource examples resolve from that package or workspace root. -->

## Understandable

### Page language (3.1.1)

```html
<!-- ❌ No language specified -->
<html>
  <!-- ✅ Language specified -->
  <html lang="en">
    <!-- ✅ Language changes within page -->
    <p>The French word for hello is <span lang="fr">bonjour</span>.</p>
  </html>
</html>
```

### Consistent navigation (3.2.3)

```html
<!-- Navigation should be consistent across pages -->
<nav aria-label="Main">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

### Form labels (3.3.2)

```html
<!-- ❌ No label association -->
<input type="email" placeholder="Email" />

<!-- ✅ Explicit label -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" autocomplete="email" required />

<!-- ✅ Implicit label -->
<label>
  Email address
  <input type="email" name="email" autocomplete="email" required />
</label>

<!-- ✅ With instructions -->
<label for="password">Password</label>
<input type="password" id="password" aria-describedby="password-requirements" />
<p id="password-requirements">Must be at least 8 characters with one number.</p>
```

### Error handling (3.3.1, 3.3.3)

```html
<!-- Announce errors to screen readers -->
<form novalidate>
  <div class="field" aria-live="polite">
    <label for="email">Email</label>
    <input type="email" id="email" aria-invalid="true" aria-describedby="email-error" />
    <p id="email-error" class="error" role="alert">Please enter a valid email address (e.g., name@example.com)</p>
  </div>
</form>
```

```javascript
// Focus first error on submit
form.addEventListener('submit', (e) => {
  const firstError = form.querySelector('[aria-invalid="true"]')
  if (firstError) {
    e.preventDefault()
    firstError.focus()

    // Announce error summary
    const errorSummary = document.getElementById('error-summary')
    errorSummary.textContent = `${errors.length} errors found. Please fix them and try again.`
    errorSummary.focus()
  }
})
```

---
