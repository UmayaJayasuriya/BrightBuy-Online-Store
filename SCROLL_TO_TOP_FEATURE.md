# Scroll to Top Feature Documentation

## Overview

Implemented automatic scroll-to-top behavior that triggers whenever users navigate to a different page. This enhances user experience by ensuring the top of each page is always visible upon navigation.

## Implementation Details

### Component Created

**File**: `frontend/src/components/common/ScrollToTop.jsx`

- **Purpose**: Automatically scrolls window to top on route changes
- **How it works**:
  - Uses React Router's `useLocation()` hook to detect route changes
  - Uses `useEffect()` hook to scroll window when pathname changes
  - Renders nothing (returns null) - pure utility component

### Scroll Behavior

- **Type**: `instant` (immediate scroll, no animation)
- **Position**: Top-left corner (0, 0)
- **Trigger**: Every time the URL pathname changes

### Integration

**File**: `frontend/src/App.jsx`

The `ScrollToTop` component is placed inside the `<Router>` component but outside the `<Routes>` component. This positioning ensures:

1. It has access to routing context (can use `useLocation`)
2. It stays mounted throughout the app lifecycle
3. It triggers on every route change

```jsx
<Router>
  <div className="App">
    <ScrollToTop /> {/* ← Added here */}
    <Spinner />
    <Header />
    <Navbar />
    <Routes>{/* All routes */}</Routes>
  </div>
</Router>
```

## User Experience Improvements

### Before

- Users scrolled down on Page A
- Clicked link to Page B
- Page B loaded but scroll position remained at bottom
- Users had to manually scroll up to see content

### After

- Users scrolled down on Page A
- Clicked link to Page B
- Page B loads AND automatically scrolls to top
- Users immediately see the top of the new page

## Customization Options

If you want **smooth scrolling** instead of instant:

```jsx
window.scrollTo({
  top: 0,
  left: 0,
  behavior: "smooth", // Change from 'instant' to 'smooth'
});
```

If you want to **exclude certain routes** from auto-scroll:

```jsx
useEffect(() => {
  // Don't scroll on certain paths
  if (pathname.includes("/admin") || pathname.includes("/profile")) {
    return;
  }

  window.scrollTo({
    top: 0,
    left: 0,
    behavior: "instant",
  });
}, [pathname]);
```

## Testing

To verify the feature works:

1. Navigate to any page and scroll down
2. Click a navigation link to go to a different page
3. Observe that the new page loads at the top (scroll position = 0)
4. Test with all navigation methods:
   - Navbar links
   - Footer links
   - Product cards
   - Buttons with navigation

## Browser Compatibility

✅ Works in all modern browsers (Chrome, Firefox, Safari, Edge)
✅ No external dependencies required
✅ Pure React implementation

## Performance

- **Lightweight**: No render output, minimal memory footprint
- **Efficient**: Only runs on route changes, not on every render
- **No delays**: Instant scroll doesn't block page rendering
