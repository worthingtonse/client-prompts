# CloudCoin Themes

This directory contains theme configurations for CloudCoin applications. Themes allow complete customization of the application's appearance including colors, images, fonts, and branding.

## Directory Structure

```
THEMES/
├── README.md                 # This file - theme documentation
├── default/                  # Default CloudCoin theme
│   ├── Theme.txt
│   └── assets/
│       ├── images/
│       └── fonts/
├── ethbold/                  # EthBold branded theme
│   ├── Theme.txt
│   └── assets/
├── light/                    # Light theme variant
│   ├── Theme.txt
│   └── assets/
└── dark/                     # Dark theme variant
    ├── Theme.txt
    └── assets/
```

## Available Themes

### Default Theme
- **Name**: CloudCoin Default
- **Style**: Official CloudCoin branding
- **Colors**: Blue and white color scheme
- **Use Case**: Standard CloudCoin applications

### EthBold Theme  
- **Name**: EthBold Wallet
- **Style**: Professional dark theme
- **Colors**: Dark background with red accents
- **Use Case**: EthBold branded applications

### Light Theme
- **Name**: CloudCoin Light
- **Style**: Clean light interface
- **Colors**: White background with blue accents
- **Use Case**: Users preferring light interfaces

### Dark Theme
- **Name**: CloudCoin Dark
- **Style**: Modern dark interface
- **Colors**: Dark background with cyan accents
- **Use Case**: Users preferring dark interfaces

## Using Themes

### Loading a Theme
```bash
# Load specific theme
load-theme "/path/to/themes/ethbold"

# Load default theme
load-theme "/path/to/themes/default"
```

### Theme Configuration
Each theme directory must contain:
1. **Theme.txt** - Main configuration file (required)
2. **assets/** - Directory containing theme assets (optional)
   - **images/** - Image files (logos, icons, backgrounds)
   - **fonts/** - Font files (TTF, OTF, WOFF)

## Creating Custom Themes

### 1. Create Theme Directory
```bash
mkdir /path/to/themes/mytheme
mkdir /path/to/themes/mytheme/assets
mkdir /path/to/themes/mytheme/assets/images
mkdir /path/to/themes/mytheme/assets/fonts
```

### 2. Create Theme.txt Configuration
```ini
[general]
name=MyTheme
title=My Custom Theme
version=1.0.0
author=Your Name

[images]
logo=assets/images/logo.png
icon=assets/images/icon.png

[colors]
backgroundcolor=#FFFFFF
maintextcolor=#000000
primarybuttoncolor=#007ACC

[fonts]
mainfont=assets/fonts/main-font.ttf

[support]
supportemail=support@example.com
```

### 3. Add Theme Assets
- Place images in `assets/images/`
- Place fonts in `assets/fonts/`
- Use relative paths in Theme.txt

### 4. Test Theme
```bash
load-theme "/path/to/themes/mytheme"
```

## Theme Requirements

### Required Sections
- `[general]` - Basic theme information
- `[colors]` - Color scheme definition
- `[fonts]` - Font specifications

### Required Keys
- `general.name` - Unique theme identifier
- `general.title` - Display name
- `colors.backgroundcolor` - Main background color
- `colors.maintextcolor` - Primary text color  
- `fonts.mainfont` - Primary font file

### Optional Sections
- `[images]` - Image and icon assets
- `[support]` - Support contact information

## Asset Guidelines

### Images
- **Formats**: PNG (preferred), JPG, SVG, ICO
- **Logo**: Transparent background PNG recommended
- **Icons**: 24x24, 32x32, 48x48 pixel variants
- **Backgrounds**: High resolution for various screen sizes

### Fonts
- **Formats**: TTF, OTF (preferred), WOFF, WOFF2
- **Variants**: Regular, bold, semi-bold recommended
- **License**: Ensure proper licensing for distribution

### Colors
- **Format**: Hex colors (#RRGGBB) preferred
- **Contrast**: Ensure sufficient contrast for accessibility
- **Consistency**: Use consistent color palette throughout

## Theme Validation

Themes are validated for:
- ✅ Required sections and keys present
- ✅ Valid color formats
- ✅ Asset file existence
- ✅ Font file accessibility
- ✅ Proper directory structure

## Theme Examples

### Minimal Theme
```ini
[general]
name=Minimal
title=Minimal Theme

[colors]
backgroundcolor=#FFFFFF
maintextcolor=#000000

[fonts]
mainfont=system-default
```

### Complete Theme
```ini
[general]
name=Complete
title=Complete Theme Example
version=2.1.0
author=CloudCoin Team
description=A fully configured theme

[images]
logo=assets/images/logo.png
icon=assets/images/icon.png
backgroundimage=assets/images/background.jpg

[colors]
backgroundcolor=#2C303D
maintextcolor=#D4D4D4
primarybuttoncolor=#AB0000
errorcolor=#FF0000

[fonts]
mainfont=assets/fonts/Roboto-Regular.ttf
mainfontbold=assets/fonts/Roboto-Bold.ttf

[support]
supportemail=support@cloudcoin.org
supportpage=https://cloudcoin.org/support
```

## Troubleshooting

### Common Issues

**Theme not loading**
- Check Theme.txt file exists
- Verify directory permissions
- Check INI file syntax

**Missing assets**
- Verify asset files exist in correct paths
- Check file permissions
- Ensure proper file extensions

**Invalid colors**
- Use proper hex format (#RRGGBB)
- Check for typos in color values
- Validate RGB/RGBA syntax

**Font issues**
- Ensure font files are accessible
- Check font file formats (TTF/OTF preferred)
- Verify font licensing

### Validation Errors

The theme loader will report specific errors:
- Missing required sections
- Invalid color formats
- Missing asset files
- Permission issues

Check the validation object in the theme loader response for detailed error information.

## Best Practices

### Theme Design
- 🎨 **Consistent Color Palette**: Use 3-5 main colors
- 🖼️ **Optimized Images**: Compress images for performance
- 🔤 **Readable Fonts**: Ensure good readability
- ♿ **Accessibility**: Maintain sufficient color contrast
- 📱 **Responsive**: Test on different screen sizes

### Theme Development
- 📁 **Organized Structure**: Keep assets well organized
- 🏷️ **Version Control**: Version your themes properly
- 📝 **Documentation**: Document theme purpose and usage
- 🧪 **Testing**: Test themes thoroughly before deployment
- 🔄 **Updates**: Keep themes updated with new features

### Theme Distribution
- 📦 **Packaging**: Include all required assets
- 📋 **Licensing**: Clear licensing information
- 🛠️ **Installation**: Provide clear installation instructions
- 🐛 **Support**: Offer support for theme issues

## Contributing

To contribute a new theme:
1. Create theme following the guidelines above
2. Test theme thoroughly
3. Include proper documentation
4. Submit theme with clear licensing
5. Provide preview screenshots

For questions about theme development, refer to the theme-file-format.md specification in the CONTEXT folder.