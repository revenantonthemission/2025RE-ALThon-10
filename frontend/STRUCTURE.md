# Frontend Structure

## Overview
The application pages have been organized and componentized for better maintainability and code reuse.

## Folder Structure

```
frontend/
├── app/
│   ├── (auth)/                    # Route group (doesn't affect URL)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page at /login
│   │   └── signup/
│   │       └── page.tsx          # Signup page at /signup
│   ├── page.tsx                  # Home page at /
│   ├── layout.tsx
│   └── globals.css
│
└── components/
    ├── auth/                     # Reusable auth components
    │   ├── auth-card.tsx         # Card wrapper for auth pages
    │   ├── form-input.tsx        # Input field with icon and error
    │   ├── icons.tsx             # Icon components
    │   └── social-login-button.tsx  # Google login button
    │
    └── landing/                  # Landing page components
        ├── navbar.tsx            # Top navigation bar
        ├── hero.tsx              # Main hero section
        └── features.tsx          # Features grid section
```

## Route Groups

The `(auth)` folder is a **route group** in Next.js (indicated by parentheses). This means:
- ✅ It organizes related routes together
- ✅ URLs remain clean: `/login` and `/signup` (not `/auth/login`)
- ✅ Shared layouts can be added at `app/(auth)/layout.tsx` if needed
- ✅ Better code organization without affecting routing

## Components

### Auth Components
See `components/auth/` for reusable authentication UI elements like cards, inputs, and buttons.

### Landing Components
The landing page is composed of:
- `LandingNavbar`: Navigation header
- `LandingHero`: Main welcome area
- `LandingFeatures`: Feature grid display

## Pages

### Home (`/`)
- Composed of landing components
- Responsive layout
- Links to login/signup

### Login (`/login`)
- Email and password fields
- "Remember me" checkbox
- "Forgot password" link
- Google sign-in button
- Link to signup page

### Signup (`/signup`)
- Full name field
- Email and password fields
- Confirm password field
- Terms and conditions checkbox
- Google sign-up button
- Link to login page

## Form Validation

Auth pages use:
- **react-hook-form** for form management
- **Zod** for schema validation
- **@hookform/resolvers** for integration

## Styling

All components use daisyUI classes with the custom theme defined in `globals.css`:
- Primary color for main actions
- Consistent spacing and typography
- Responsive design
- Dark mode support (via theme)

