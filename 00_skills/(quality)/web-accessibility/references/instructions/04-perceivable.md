<!-- Package: 00_skills/(quality)/web-accessibility; relative command/resource examples resolve from that package or workspace root. -->

## Perceivable

### Text alternatives (1.1)

**Images require alt text:**

```html
<!-- ❌ Missing alt -->
<img src="chart.png" />

<!-- ✅ Descriptive alt -->
<img src="chart.png" alt="Bar chart showing 40% increase in Q3 sales" />

<!-- ✅ Decorative image (empty alt) -->
<img src="decorative-border.png" alt="" role="presentation" />

<!-- ✅ Complex image with longer description -->
<figure>
  <img src="infographic.png" alt="2024 market trends infographic" aria-describedby="infographic-desc" />
  <figcaption id="infographic-desc">
    <!-- Detailed description -->
  </figcaption>
</figure>
```

**Icon buttons need accessible names:**

```html
<!-- ❌ No accessible name -->
<button>
  <svg><!-- menu icon --></svg>
</button>

<!-- ✅ Using aria-label -->
<button aria-label="Open menu">
  <svg aria-hidden="true"><!-- menu icon --></svg>
</button>

<!-- ✅ Using visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- menu icon --></svg>
  <span class="visually-hidden">Open menu</span>
</button>
```

**Visually hidden class:**

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### Color contrast (1.4.3, 1.4.6)

| Text Size                          | AA minimum | AAA enhanced |
| ---------------------------------- | ---------- | ------------ |
| Normal text (< 18px / < 14px bold) | 4.5:1      | 7:1          |
| Large text (≥ 18px / ≥ 14px bold)  | 3:1        | 4.5:1        |
| UI components & graphics           | 3:1        | 3:1          |

```css
/* ❌ Low contrast (2.5:1) */
.low-contrast {
  color: #999;
  background: #fff;
}

/* ✅ Sufficient contrast (7:1) */
.high-contrast {
  color: #333;
  background: #fff;
}

/* ✅ Focus states need contrast too */
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}
```

**Don't rely on color alone:**

```html
<!-- ❌ Only color indicates error -->
<input class="error-border" />
<style>
  .error-border {
    border-color: red;
  }
</style>

<!-- ✅ Color + icon + text -->
<div class="field-error">
  <input aria-invalid="true" aria-describedby="email-error" />
  <span id="email-error" class="error-message">
    <svg aria-hidden="true"><!-- error icon --></svg>
    Please enter a valid email address
  </span>
</div>
```

### Media alternatives (1.2)

```html
<!-- Video with captions -->
<video controls>
  <source src="video.mp4" type="video/mp4" />
  <track kind="captions" src="captions.vtt" srclang="en" label="English" default />
  <track kind="descriptions" src="descriptions.vtt" srclang="en" label="Descriptions" />
</video>

<!-- Audio with transcript -->
<audio controls>
  <source src="podcast.mp3" type="audio/mp3" />
</audio>
<details>
  <summary>Transcript</summary>
  <p>Full transcript text...</p>
</details>
```

---
