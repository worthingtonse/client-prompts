# Apply Theme Function Prompt

This is used to create a function called `apply-theme(theme_object: object, application_context: object)`. This function takes two arguments: a theme object (returned from load-theme) and an application context object.

The primary purpose of this function is to apply a loaded theme configuration to an active application, updating the user interface elements, colors, fonts, images, and other visual aspects according to the theme specifications.

## Function Requirements

### 1. Theme Object Processing
The function must accept a theme object with the structure returned by the load-theme function.
Process all theme sections: general, images, colors, fonts, and support information.
Handle missing or invalid theme properties gracefully with fallback values.

### 2. Application Context Integration
The function needs to work with different application contexts (desktop, web, mobile).
Apply theme changes to the appropriate UI framework or rendering system.
Maintain application state and functionality while updating visual appearance.

### 3. Dynamic UI Updates
Update colors throughout the application interface in real-time.
Replace images and icons with theme-specific assets.
Change fonts and typography across all text elements.
Apply branding and support information updates.

### 4. Return Value
The function must return a status object indicating success/failure and any issues encountered during theme application.

## Input Parameters

- **theme_object** (object): Complete theme configuration object from load-theme function
- **application_context** (object): Application-specific context containing UI references and configuration

## Output
(object): Status object containing application results and any errors or warnings

## Application Context Structure

The application_context object contains platform-specific UI references:

```json
{
  "platform": "desktop|web|mobile",
  "ui_framework": "electron|qt|web|react|flutter",
  "ui_elements": {
    "main_window": "reference_to_main_window",
    "stylesheet": "reference_to_css_or_style_system",
    "image_cache": "reference_to_image_caching_system",
    "font_loader": "reference_to_font_loading_system"
  },
  "capabilities": {
    "supports_custom_fonts": true,
    "supports_dynamic_colors": true,
    "supports_image_replacement": true,
    "requires_restart": false
  }
}
```

## Detailed Logic Flow

### 1. Validate Input Parameters
- Verify theme_object is valid and contains required sections
- Check application_context contains necessary UI references
- Validate platform compatibility with theme features

### 2. Prepare Theme Application
- Create backup of current theme settings (for rollback)
- Initialize change tracking for status reporting
- Prepare asset loading queues

### 3. Apply Color Scheme
- Update background colors for all UI panels and windows
- Change text colors for all text elements
- Update button and interactive element colors
- Apply hover and active state colors
- Modify border and separator colors

### 4. Replace Images and Icons
- Load and cache new image assets
- Replace application logos and branding images
- Update all UI icons with theme-specific versions
- Handle missing images with fallback assets
- Update icon states (normal, hover, active, disabled)

### 5. Update Typography
- Load custom font files if supported
- Apply font families to all text elements
- Update font weights and styles
- Handle font fallbacks for unsupported platforms

### 6. Apply Branding Information
- Update application title and branding text
- Apply support contact information
- Update help and documentation links
- Modify about dialogs and version information

### 7. Handle Platform-Specific Requirements
- Apply CSS changes for web applications
- Update native UI elements for desktop applications
- Handle mobile-specific UI adaptations
- Trigger UI refresh or repaint as needed

### 8. Validate Application Results
- Verify all changes were applied successfully
- Check for any visual or functional issues
- Create status report with success/failure information

### 9. Return Status Object
- Report successful theme application
- Include any warnings or partial failures
- Provide rollback information if needed

## Color Application Details

### Background Colors
```javascript
// Apply main background
application.setBackgroundColor(theme.colors.backgroundcolor);

// Apply header background  
application.setHeaderBackground(theme.colors.headerbackgroundcolor);

// Apply panel backgrounds
application.setPanelBackground(theme.colors.panelbackgroundcolor);
```

### Text Colors
```javascript
// Apply primary text color
application.setTextColor('primary', theme.colors.maintextcolor);

// Apply secondary text color
application.setTextColor('secondary', theme.colors.secondtextcolor);

// Apply title text color
application.setTextColor('title', theme.colors.titletextcolor);
```

### Interactive Element Colors
```javascript
// Apply button colors
application.setButtonColor('primary', theme.colors.primarybuttoncolor);
application.setButtonColor('secondary', theme.colors.secondarybuttoncolor);

// Apply hover states
application.setHoverColor('menu', theme.colors.topmenuhovercolor);
```

## Font Application Details

### Font Loading
```javascript
// Load custom fonts
for (const [fontType, fontPath] of Object.entries(theme.fonts)) {
    application.loadFont(fontType, fontPath);
}

// Apply fonts to elements
application.setFont('body', theme.fonts.mainfont);
application.setFont('heading', theme.fonts.mainfontbold);
```

### Font Fallbacks
```javascript
// Define fallback fonts for different platforms
const fallbackFonts = {
    'windows': 'Segoe UI, sans-serif',
    'macos': 'San Francisco, sans-serif', 
    'linux': 'Ubuntu, sans-serif',
    'web': 'system-ui, sans-serif'
};
```

## Image Application Details

### Image Replacement
```javascript
// Replace application images
for (const [imageType, imagePath] of Object.entries(theme.images)) {
    application.setImage(imageType, imagePath);
}

// Handle missing images
application.onImageLoadError((imageType, error) => {
    application.setImage(imageType, getDefaultImage(imageType));
    logWarning(`Image ${imageType} not found, using default`);
});
```

### Icon Updates
```javascript
// Update toolbar icons
application.setToolbarIcon('deposit', theme.images.depositicon);
application.setToolbarIcon('withdraw', theme.images.withdrawicon);

// Update hover states
application.setToolbarIconHover('deposit', theme.images.depositiconhover);
```

## Platform-Specific Implementation

### Web Applications
```javascript
// Apply CSS variables for colors
document.documentElement.style.setProperty('--bg-color', theme.colors.backgroundcolor);
document.documentElement.style.setProperty('--text-color', theme.colors.maintextcolor);

// Load custom fonts
const fontFace = new FontFace('CustomFont', `url(${theme.fonts.mainfont})`);
document.fonts.add(fontFace);
```

### Desktop Applications
```javascript
// Update native window properties
window.setBackgroundColor(theme.colors.backgroundcolor);
window.setTitle(theme.general.title);

// Apply native stylesheets
application.setStyleSheet(generateStyleSheet(theme));
```

### Mobile Applications
```javascript
// Update status bar and navigation
application.setStatusBarStyle(theme.colors.headerbackgroundcolor);
application.setNavigationBarColor(theme.colors.backgroundcolor);
```

## Error Handling and Fallbacks

### Color Fallbacks
```javascript
const defaultColors = {
    backgroundcolor: '#FFFFFF',
    maintextcolor: '#000000',
    primarybuttoncolor: '#007ACC',
    errorcolor: '#FF0000'
};

function applyColorWithFallback(element, colorKey, themeColor) {
    const color = themeColor || defaultColors[colorKey];
    element.setColor(color);
}
```

### Asset Fallbacks
```javascript
function loadImageWithFallback(imageType, imagePath) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(imagePath);
        img.onerror = () => {
            const fallback = getDefaultAsset(imageType);
            resolve(fallback);
        };
        img.src = imagePath;
    });
}
```

## Return Status Object

```json
{
  "success": true,
  "theme_applied": "EthBold",
  "timestamp": "2025-01-15T10:30:00Z",
  "changes_applied": {
    "colors_updated": 25,
    "images_replaced": 15,
    "fonts_loaded": 3,
    "branding_updated": true
  },
  "warnings": [
    "Background image not found, using default",
    "Custom font not supported on this platform"
  ],
  "errors": [],
  "rollback_available": true,
  "platform_specific": {
    "requires_restart": false,
    "performance_impact": "minimal"
  }
}
```

## Error Response Example

```json
{
  "success": false,
  "error": "Theme application failed",
  "details": "Invalid color format in theme.colors.backgroundcolor",
  "changes_applied": {
    "colors_updated": 5,
    "images_replaced": 0,
    "fonts_loaded": 0,
    "branding_updated": false
  },
  "rollback_performed": true,
  "rollback_successful": true
}
```

## Integration Notes

- This function works in conjunction with load-theme to provide complete theming
- Supports hot-swapping themes without application restart (where possible)
- Can be used for real-time theme preview functionality
- Maintains application state and user data during theme changes
- Provides foundation for theme customization interfaces
- Supports undo/redo operations through rollback mechanisms