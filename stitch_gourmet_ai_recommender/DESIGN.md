---
name: Lumina Gastronomy AI
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#3a393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353436'
  on-surface: '#e5e2e3'
  on-surface-variant: '#d1c2d2'
  inverse-surface: '#e5e2e3'
  inverse-on-surface: '#313031'
  outline: '#9a8c9b'
  outline-variant: '#4e4350'
  surface-tint: '#edb1ff'
  primary: '#edb1ff'
  on-primary: '#520070'
  primary-container: '#9d50bb'
  on-primary-container: '#fff3fd'
  inverse-primary: '#883ca6'
  secondary: '#d6baff'
  on-secondary: '#40147a'
  secondary-container: '#573092'
  on-secondary-container: '#c7a5ff'
  tertiary: '#47d6ff'
  on-tertiary: '#003543'
  tertiary-container: '#007b97'
  on-tertiary-container: '#ebf9ff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#f9d8ff'
  primary-fixed-dim: '#edb1ff'
  on-primary-fixed: '#320046'
  on-primary-fixed-variant: '#6e208c'
  secondary-fixed: '#ecdcff'
  secondary-fixed-dim: '#d6baff'
  on-secondary-fixed: '#270057'
  on-secondary-fixed-variant: '#573092'
  tertiary-fixed: '#b6ebff'
  tertiary-fixed-dim: '#47d6ff'
  on-tertiary-fixed: '#001f28'
  on-tertiary-fixed-variant: '#004e60'
  background: '#131314'
  on-background: '#e5e2e3'
  surface-variant: '#353436'
typography:
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '800'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.1em
  button-text:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
---

## Brand & Style
The design system embodies a premium, futuristic concierge experience. It targets a discerning audience seeking high-fidelity restaurant discovery powered by artificial intelligence. 

The visual style is a fusion of **Glassmorphism** and **High-Contrast Modernism**. The UI should feel like a high-end digital cockpit—sophisticated, responsive, and ethereal. By utilizing deep obsidian surfaces punctuated by neon atmospheric glows, the design system evokes a sense of "digital luxury" and cutting-edge precision. Every interaction should feel intentional, with depth created through transparency rather than traditional heavy shadows.

## Colors
The palette is anchored in a "Deep Charcoal" (#0A0A0B) to ensure maximum contrast for neon elements and deep black levels on OLED displays. 

- **Primary & Secondary:** A sunset-to-midnight purple gradient serves as the core brand identifier, used for primary actions and AI-driven highlights.
- **Tertiary:** An "Electric Blue" is used sparingly for data visualization, success states, or subtle navigational cues to prevent the interface from feeling monochromatic.
- **Glass Effects:** Surfaces utilize a semi-transparent white stroke (#FFFFFF at 8-12% opacity) to define edges against the dark background, mimicking the physical properties of machined glass.

## Typography
This design system utilizes **Plus Jakarta Sans** exclusively to maintain a clean, geometric, and modern feel. 

- **Headlines:** Use tighter letter-spacing and bold weights to command attention. High-end restaurant names should feel architectural.
- **Body:** Use a slightly increased line-height (1.6) to ensure readability against dark backgrounds, preventing "halation" (where light text appears to bleed into the dark).
- **Labels:** Small caps with wide tracking are used for metadata like "CUISINE TYPE" or "DISTANCE" to provide a technical, futuristic look without cluttering the hierarchy.

## Layout & Spacing
The layout follows a **Fluid Grid** model with generous internal padding to maintain a "breathable" premium feel.

- **Desktop:** 12-column grid with 24px gutters. Content is centered with a max-width of 1280px.
- **Mobile:** 4-column grid with 20px side margins. 
- **Rhythm:** All spacing (margins, padding, gaps) must be multiples of 8px. Use larger gaps (48px+) between distinct content sections to reinforce the minimalist aesthetic.
- **AI Chat Interface:** The central interaction point should be anchored at the bottom with a floating, glass-morphic input bar that spans 8 columns on desktop.

## Elevation & Depth
Depth is achieved through **Backdrop Filtering** and **Luminance** rather than traditional drop shadows.

1.  **Level 0 (Base):** The #0A0A0B background.
2.  **Level 1 (Cards/Panels):** Background blur (20px) with a `rgba(255, 255, 255, 0.03)` fill and a 1px solid `rgba(255, 255, 255, 0.08)` border.
3.  **Level 2 (Modals/Active States):** Increased blur (40px) with a subtle inner glow using the primary purple color at 10% opacity.
4.  **Atmospheric Glow:** Large, blurry radial gradients (300px-600px radius) in primary/secondary colors are placed far behind the UI layers to create a sense of environmental lighting.

## Shapes
The shape language is consistently **Rounded** (0.5rem base) to feel approachable yet sleek. 

- **Standard Elements:** Buttons, inputs, and small cards use a 8px (0.5rem) radius.
- **Large Containers:** Main restaurant cards and the AI chat bubble use `rounded-xl` (24px/1.5rem) to feel softer and more organic.
- **Interactive States:** When hovered, elements can subtly increase their corner radius or expand slightly (1.02x scale) to indicate "life" within the interface.

## Components

- **AI Input Field:** A pill-shaped component with a thick backdrop-blur (saturate 180%). The border should animate with a purple-to-blue gradient stroke when focused.
- **Action Buttons:** 
    - *Primary:* Solid sunset gradient with a white label. Includes a soft outer glow of the same color.
    - *Secondary:* Glassmorphic (clear fill, white border) with high-contrast white text.
- **Restaurant Cards:** High-quality photography with a dark-to-transparent gradient overlay at the bottom. Typography for the restaurant name and rating is overlaid directly on the card.
- **Status Chips:** Small, semi-transparent capsules for "Open Now" or "Trending." Use the Tertiary Blue for technical status and Primary Purple for curated recommendations.
- **The "Pulse":** An animated component for the AI's "thinking" state, represented by a soft, breathing glow effect behind the logo or the input area.
- **Lists:** Clean, borderless rows separated by 1px lines at 5% white opacity. Iconography should be thin-stroke (1.5pt) to match the high-fidelity typography.