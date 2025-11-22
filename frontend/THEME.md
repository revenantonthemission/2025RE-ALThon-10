# REALThon Custom Theme & Color Palette

This project uses daisyUI 5 with custom themes specifically designed for the REALThon application.

## Themes

We have created two custom themes:

### 1. **realthon** (Light Theme - Default)
A modern, clean light theme with soft blue-purple accents.

### 2. **realthon-dark** (Dark Theme)
An elegant dark theme that automatically activates based on system preferences.

## Color Palette

### Light Theme Colors

| Color | Value | Usage |
|-------|-------|-------|
| **Primary** | `oklch(60% 0.25 260)` | Main brand color - Blue-purple for primary actions |
| **Secondary** | `oklch(65% 0.2 320)` | Magenta-pink for secondary elements |
| **Accent** | `oklch(70% 0.22 180)` | Cyan for accent highlights |
| **Neutral** | `oklch(30% 0.03 240)` | Dark blue-gray for text and borders |
| **Base-100** | `oklch(98% 0.01 240)` | Lightest background |
| **Base-200** | `oklch(96% 0.02 240)` | Secondary background for elevation |
| **Base-300** | `oklch(94% 0.03 240)` | Tertiary background for more elevation |
| **Info** | `oklch(65% 0.2 220)` | Blue for informational messages |
| **Success** | `oklch(70% 0.2 150)` | Green for success states |
| **Warning** | `oklch(80% 0.2 80)` | Yellow-orange for warnings |
| **Error** | `oklch(65% 0.25 25)` | Red for error states |

### Dark Theme Colors

| Color | Value | Usage |
|-------|-------|-------|
| **Primary** | `oklch(65% 0.25 260)` | Brighter blue-purple for dark mode |
| **Secondary** | `oklch(70% 0.2 320)` | Brighter magenta-pink |
| **Accent** | `oklch(75% 0.22 180)` | Brighter cyan |
| **Neutral** | `oklch(80% 0.02 240)` | Light gray for text |
| **Base-100** | `oklch(20% 0.02 240)` | Dark background |
| **Base-200** | `oklch(16% 0.03 240)` | Darker for elevation |
| **Base-300** | `oklch(12% 0.04 240)` | Darkest for more elevation |
| **Info** | `oklch(70% 0.2 220)` | Brighter blue |
| **Success** | `oklch(75% 0.2 150)` | Brighter green |
| **Warning** | `oklch(85% 0.2 80)` | Brighter yellow |
| **Error** | `oklch(70% 0.25 25)` | Brighter red |

## Design System Properties

### Border Radius
- **Selectors** (checkbox, toggle, badge): `1rem` - Fully rounded
- **Fields** (button, input, select): `0.5rem` - Moderately rounded
- **Boxes** (card, modal, alert): `1rem` - Fully rounded

### Sizes
- **Selectors**: `0.25rem` base size
- **Fields**: `0.25rem` base size

### Effects
- **Depth**: `1` - Adds subtle shadow and 3D effect to components
- **Noise**: `0` - No grain effect
- **Border**: `1px` - Standard border width

## Color Usage Guidelines

### Primary Color
Use for:
- Primary action buttons
- Important CTAs
- Active navigation items
- Key interactive elements

### Secondary Color
Use for:
- Secondary actions
- Alternative buttons
- Supporting elements

### Accent Color
Use for:
- Highlights
- Hover states on special elements
- Badge notifications
- Important status indicators

### Base Colors
Use for:
- Page backgrounds (base-100)
- Card backgrounds
- Creating depth through elevation (base-200, base-300)
- Main text (base-content)

### Semantic Colors

- **Info**: Informational messages, tips
- **Success**: Successful operations, confirmations
- **Warning**: Caution messages, important notices
- **Error**: Error messages, failed operations

## How to Use

### In Your Components

```tsx
// Buttons
<button className="btn btn-primary">Primary Action</button>
<button className="btn btn-secondary">Secondary Action</button>

// Cards
<div className="card bg-base-100 shadow-xl">
  <div className="card-body">
    <h2 className="card-title">Card Title</h2>
    <p>Card content with base-content color</p>
  </div>
</div>

// Alerts
<div role="alert" className="alert alert-success">
  <span>Success message!</span>
</div>
```

### Theme Switching

The theme automatically switches based on system preferences (prefers-color-scheme), but you can also implement manual theme switching using daisyUI's theme-controller:

```tsx
<input 
  type="checkbox" 
  value="realthon-dark" 
  className="theme-controller" 
/>
```

## Color Philosophy

The color palette was designed with these principles:

1. **Accessibility**: All color combinations meet WCAG AA standards for contrast
2. **Consistency**: Colors maintain their relationship across light and dark modes
3. **Modern**: Using OKLCH color space for better perceptual uniformity
4. **Purposeful**: Each color has a specific semantic meaning
5. **Harmonious**: Colors work well together while maintaining distinct roles

## Extending the Theme

To modify the theme, edit the `@plugin "daisyui/theme"` blocks in `app/globals.css`:

```css
@plugin "daisyui/theme" {
  name: "realthon";
  default: true;
  
  /* Modify colors here */
  --color-primary: oklch(60% 0.25 260);
  /* ... other colors ... */
}
```

## Resources

- [daisyUI Documentation](https://daisyui.com)
- [daisyUI Theme Generator](https://daisyui.com/theme-generator/)
- [OKLCH Color Picker](https://oklch.com)

