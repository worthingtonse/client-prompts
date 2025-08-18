# CloudCoin Themes

This directory contains theme configurations for CloudCoin applications. Themes allow complete customization of the application's appearance including colors, images, fonts, and branding.

## Directory Structure

Based on the CloudCoin Pro program structure, themes are located at:

```
D:/CloudCoin/Pro/
├── Wallets/
├── Themes/                       # Theme directory at Pro level
│   ├── README.md                 # This file - theme documentation
│   ├── default/                  # Default CloudCoin theme
│   │   ├── Theme.txt
│   │   └── assets/
│   │       ├── images/
│   │       └── fonts/
│   ├── light/                    # Light theme for bright environments
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── dark/                     # Dark theme for low-light environments
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── high-contrast/            # High contrast theme for accessibility
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── forest/                   # Nature-inspired green theme
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── ocean/                    # Blue ocean-inspired theme
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── sunset/                   # Warm orange/red theme
│   │   ├── Theme.txt
│   │   └── assets/
│   ├── ethbold/                  # EthBold branded theme
│   │   ├── Theme.txt
│   │   └── assets/
│   └── custom/                   # User custom themes folder
│       ├── mytheme1/
│       ├── mytheme2/
│       └── README.md
├── Client Server Keys/
├── Receipts/
└── [other Pro directories...]
```

## Available Built-in Themes

### 🌟 Default Theme
- **Name**: CloudCoin Default
- **Style**: Official CloudCoin branding
- **Colors**: Blue and white color scheme
- **Use Case**: Standard CloudCoin applications
- **Accessibility**: WCAG AA compliant

### ☀️ Light Theme  
- **Name**: CloudCoin Light
- **Style**: Clean, bright interface
- **Colors**: White backgrounds, dark text, blue accents
- **Use Case**: Well-lit environments, users preferring light interfaces
- **Features**: High readability, minimal eye strain in bright light

### 🌙 Dark Theme
- **Name**: CloudCoin Dark
- **Style**: Modern dark interface
- **Colors**: Dark backgrounds, light text, cyan accents
- **Use Case**: Low-light environments, users preferring dark interfaces
- **Features**: Reduced eye strain, battery saving on OLED screens

### ♿ High Contrast Theme
- **Name**: CloudCoin High Contrast
- **Style**: Maximum contrast for accessibility
- **Colors**: Black/white with bright accent colors
- **Use Case**: Users with visual impairments, accessibility compliance
- **Features**: WCAG AAA compliant, enhanced readability

### 🌲 Forest Theme
- **Name**: CloudCoin Forest
- **Style**: Nature-inspired green theme
- **Colors**: Various shades of green with earth tones
- **Use Case**: Users who prefer natural, calming colors
- **Features**: Relaxing color palette, eco-friendly appearance

### 🌊 Ocean Theme
- **Name**: CloudCoin Ocean
- **Style**: Ocean-inspired blue theme
- **Colors**: Deep blues, teals, and aqua tones
- **Use Case**: Professional appearance with calming blue tones
- **Features**: Trust-inspiring, corporate-friendly colors

### 🌅 Sunset Theme
- **Name**: CloudCoin Sunset
- **Style**: Warm sunset colors
- **Colors**: Orange, red, and warm yellow tones
- **Use Case**: Users preferring warm, energetic colors
- **Features**: Vibrant, inspiring color palette

### 🏢 EthBold Theme  
- **Name**: EthBold Wallet
- **Style**: Professional dark theme with red accents
- **Colors**: Dark background with red branding
- **Use Case**: EthBold branded applications
- **Features**: Corporate branding, professional appearance

## Theme Categories

### Accessibility Themes
- **High Contrast**: Maximum contrast for vision accessibility
- **Large Text**: Bigger fonts for readability
- **Colorblind Friendly**: Colors chosen for colorblind users

### Environment Themes  
- **Bright Environment**: Light theme optimized for daylight
- **Dark Environment**: Dark theme for low-light conditions
- **Auto Switching**: Automatically switches based on time/ambient light

### Style Themes
- **Minimalist**: Clean, simple design with minimal elements
- **Vibrant**: Bold, colorful design with rich graphics
- **Corporate**: Professional, business-appropriate styling
- **Gaming**: High-energy theme with gaming aesthetics

### Custom User Themes
- **User Created**: Themes created by users
- **Community Shared**: Themes shared by the community
- **Brand Specific**: Themes for specific organizations

## Using Themes

### Loading a Theme
```bash
# Load specific theme from Pro directory
load-theme "D:/CloudCoin/Pro/Themes/dark"

# Load user custom theme
load-theme "D:/CloudCoin/Pro/Themes/custom/mytheme"

# Load default theme
load-theme "D:/CloudCoin/Pro/Themes/default"
```

### Theme Configuration Path
All themes are located under the main CloudCoin Pro installation:
```
D:/CloudCoin/Pro/Themes/{theme-name}/Theme.txt
```

## Creating Custom Themes

### 1. Create Custom Theme Directory
```bash
# Create in the custom themes folder
mkdir "D:/CloudCoin/Pro/Themes/custom/mytheme"
mkdir "D:/CloudCoin/Pro/Themes/custom/mytheme/assets"
mkdir "D:/CloudCoin/Pro/Themes/custom/mytheme/assets/images"
mkdir "D:/CloudCoin/Pro/Themes/custom/mytheme/assets/fonts"
```

### 2. Create Theme.txt Configuration
```ini
[general]
name=MyCustomTheme
title=My Custom Theme
version=1.0.0
author=Your Name
description=My personalized CloudCoin theme

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
validate-theme "D:/CloudCoin/Pro/Themes/custom/mytheme"
load-theme "D:/CloudCoin/Pro/Themes/custom/mytheme"
```

## Built-in Theme Examples

### Quick Theme Switching
Users can quickly switch between pre-built themes:

```bash
# Switch to dark mode for evening use
apply-theme dark

# Switch to high contrast for accessibility
apply-theme high-contrast

# Switch to light mode for daytime use  
apply-theme light

# Switch to forest theme for relaxing colors
apply-theme forest
```

## Theme Installation

### Installing New Themes
1. **Download theme package** (usually a ZIP file)
2. **Extract to themes directory**: `D:/CloudCoin/Pro/Themes/theme-name/`
3. **Validate theme**: Run `validate-theme` to check for issues
4. **Apply theme**: Use `load-theme` and `apply-theme` to use the new theme

### Sharing Custom Themes
1. **Package theme directory** with all assets
2. **Include README.md** with theme description and preview
3. **Test theme thoroughly** on different screen sizes
4. **Share theme package** with other users

## Theme Management Features

### Theme Preferences
- **Auto-switching**: Switch themes based on time of day
- **Environment detection**: Switch based on ambient light
- **User profiles**: Different themes for different users
- **Application modes**: Different themes for different app modes

### Theme Customization
- **Color picker**: Modify colors in real-time
- **Font selection**: Choose from installed system fonts
- **Image replacement**: Upload custom logos and icons
- **Layout options**: Modify spacing and sizing

### Theme Backup
- **Export settings**: Save current theme configuration
- **Import settings**: Restore theme from backup
- **Sync themes**: Synchronize themes across devices
- **Cloud storage**: Store themes in cloud for portability

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