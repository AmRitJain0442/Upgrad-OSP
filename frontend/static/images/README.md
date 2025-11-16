# upGrad Logo Integration Guide

## Save the Logo

Save the upGrad logo image as:
```
frontend/static/images/upgrad-logo.png
```

## Logo Specifications

**Recommended Format:**
- **Format**: PNG with transparency
- **Resolution**: 360px width (2x for retina displays)
- **File size**: Optimize to < 50KB if possible

**Display Sizes:**
- Landing page hero: 180px width (140px on mobile)
- Site header: 40px height (32px on mobile)
- Browser favicon: 32x32px (auto-resized)

## Integration Status

### ✅ Global Site Header (All Pages)
- Fixed top navigation bar
- Logo height: 40px (32px mobile)
- Navigation links: Home, Courses, Workflows
- Logo is clickable → redirects to home
- Backdrop blur effect with semi-transparent background

### ✅ Landing Page Hero
- Centered above main title
- Width: 180px (140px on mobile)
- Drop shadow: `0 4px 12px rgba(0, 0, 0, 0.15)`
- Hover animation: Scale 1.05

### ✅ Browser Favicon
- Automatically uses logo as favicon
- Appears in browser tabs
- Consistent branding

## Pages with Logo

1. **Landing Page** (`/`) - Hero logo + header
2. **Courses Page** (`/prompting/`) - Header
3. **Workflow Page** (`/prompting/workflow`) - Header
4. **Module Pages** (`/prompting/module/*`) - Header
5. **Aurora Demo** (`/aurora-demo`) - Header

All pages inherit the header with logo from `base.html`.

## Next Steps

1. ⏳ Save logo as `upgrad-logo.png` in this directory
2. ⏳ Refresh any page to see the logo
3. ✅ Logo will appear globally on all pages
4. ✅ Favicon will update automatically

## Styling Adjustments

**Landing Page Logo:** Edit `.brand-logo` class in `landing.html`
**Header Logo:** Edit `.site-logo` class in `base.html`
