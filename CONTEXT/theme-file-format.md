# Theme File Format Specification

This document defines the standard format for Theme.txt files used to customize the appearance and branding of CloudCoin applications. All theme-related functions must follow this specification to ensure consistency and compatibility.

## File Structure

Theme files use INI format with sections and key-value pairs:

```ini
[section]
key=value
key2=value2

[anothersection]
key=value
```

## Required Sections

### [general]
General theme information and metadata.

| Key | Type | Required | Description | Example |
|-----|------|----------|-------------|---------|
| name | string | Yes | Unique theme identifier | `EthBold` |
| title | string | Yes | Human-readable theme name | `EthBold Wallet` |
| version | string | No | Theme version number | `1.0.0` |
| versionoffset | integer | No | Version display offset | `0` |
| terms | string | No | Terms and conditions file | `TermsAndConditions.html` |
| author | string | No | Theme creator | `CloudCoin Team` |
| description | string | No | Theme description | `Professional dark theme` |

### [images]
Image assets used throughout the application.

| Key | Type | Required | Description | Default |
|-----|------|----------|-------------|---------|
| logo | string | Yes | Main application logo | `CloudCoinLogo.png` |
| logotext | string | No | Logo with text | `CloudCoinText.png` |
| backgroundimage | string | No | Background image | `bglogo.png` |
| icon | string | Yes | Application icon | `CloudCoinLogo.png` |

#### Navigation Icons
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| depositicon | string | No | Deposit button icon |
| withdrawicon | string | No | Withdraw button icon |
| transfericon | string | No | Transfer button icon |
| depositiconhover | string | No | Deposit hover state |
| withdrawiconhover | string | No | Withdraw hover state |
| transfericonhover | string | No | Transfer hover state |

#### Feature Icons
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| coinsinventoryicon | string | No | Coins inventory icon |
| coinsicon | string | No | General coins icon |
| supporticon | string | No | Support section icon |
| settingsicon | string | No | Settings icon |
| walletskyicon | string | No | Cloud wallet icon |
| walletlocalicon | string | No | Local wallet icon |
| vaulticon | string | No | Vault icon |
| vaulticonactive | string | No | Active vault icon |

#### Security Icons
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| lockicon | string | No | Lock/security icon |
| lockiconactive | string | No | Active lock icon |
| cloudicon | string | No | Cloud service icon |
| cloudiconactive | string | No | Active cloud icon |
| emailicon | string | No | Email icon |
| emailiconactive | string | No | Active email icon |

#### Template Images
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| templatepng | string | No | Generic PNG template |
| templatejpeg1 | string | No | 1 coin JPEG template |
| templatejpeg5 | string | No | 5 coin JPEG template |
| templatejpeg25 | string | No | 25 coin JPEG template |
| templatejpeg100 | string | No | 100 coin JPEG template |
| templatejpeg250 | string | No | 250 coin JPEG template |

#### UI Elements
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| dropdownarrow | string | No | Dropdown arrow icon |
| arrowleft | string | No | Left navigation arrow |
| arrowright | string | No | Right navigation arrow |
| toggleyes | string | No | Toggle switch ON state |
| toggleno | string | No | Toggle switch OFF state |
| lookingglass | string | No | Search icon |
| eye | string | No | Visibility toggle icon |

### [colors]
Color scheme for the application interface.

#### Background Colors
| Key | Type | Required | Description | Format |
|-----|------|----------|-------------|--------|
| backgroundcolor | color | Yes | Main background color | `#2C303D` |
| headerbackgroundcolor | color | No | Header background | `#1C1F28` |
| panelbackgroundcolor | color | No | Panel background | `#1F222B` |
| inventorybackgroundcolor | color | No | Inventory area background | `#14161E` |
| inputbackgroundcolor | color | No | Input field background | `#1B1E26` |
| dropfilesbackgroundcolor | color | No | Drag-drop area background | `#303441` |

#### Wallet Colors
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| selectedwalletbordercolor | color | No | Selected wallet border |
| activewalletbackgroundcolor | color | No | Active wallet background |
| inactivewalletbackgroundcolor | color | No | Inactive wallet background |

#### Interactive Colors
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| topmenuhovercolor | color | No | Top menu hover color |
| settingsmenuhovercolor | color | No | Settings menu hover |
| settingsmenubackgroundcolor | color | No | Settings menu background |
| dropdownhovercolor | color | No | Dropdown hover color |
| hyperlinkcolor | color | No | Hyperlink color |

#### Text Colors
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| maintextcolor | color | Yes | Primary text color |
| secondtextcolor | color | No | Secondary text color |
| thirdtextcolor | color | No | Tertiary text color |
| titletextcolor | color | No | Title text color |
| tableheadertextcolor | color | No | Table header text |
| errorcolor | color | No | Error message color |

#### Component Colors
| Key | Type | Required | Description |
|-----|------|----------|-------------|
| primarybuttoncolor | color | No | Primary button color |
| secondarybuttoncolor | color | No | Secondary button color |
| disabledbuttoncolor | color | No | Disabled button color |
| progressbarcolor | color | No | Progress bar fill color |
| progressbarbackgroundcolor | color | No | Progress bar background |
| tablegridcolor | color | No | Table grid line color |
| scrollbartrackcolor | color | No | Scrollbar track color |
| scrollbarthumbcolor | color | No | Scrollbar thumb color |

### [fonts]
Font specifications for the application.

| Key | Type | Required | Description | Example |
|-----|------|----------|-------------|---------|
| mainfont | string | Yes | Primary font file | `Montserrat-Regular.otf` |
| mainfontsemibold | string | No | Semi-bold variant | `Montserrat-SemiBold.otf` |
| mainfontbold | string | No | Bold variant | `Montserrat-Bold.otf` |
| secondfont | string | No | Secondary font | `OpenSans-Regular.ttf` |
| secondfontsemibold | string | No | Secondary semi-bold | `OpenSans-Semibold.ttf` |
| secondfontbold | string | No | Secondary bold | `OpenSans-Bold.ttf` |

### [support]
Support and contact information.

| Key | Type | Required | Description | Example |
|-----|------|----------|-------------|---------|
| supportemail | string | No | Support email address | `support@ethbold.com` |
| supportpage | string | No | Support website URL | `https://ethbold.com/use.html` |
| supporttime | string | No | Support hours | `9AM to 3PM PST` |
| supportphone | string | No | Support phone number | `+1 (530) 762-1234` |
| supportportal | string | No | Support portal URL | `https://support.ethbold.com` |

## File Format Rules

### General Rules
1. **File encoding**: UTF-8
2. **Line endings**: LF or CRLF
3. **Case sensitivity**: Keys are case-insensitive
4. **Comments**: Lines starting with `;` or `#` are ignored
5. **Whitespace**: Leading/trailing whitespace is trimmed

### Color Format
- **Hex format**: `#RRGGBB` (e.g., `#2C303D`)
- **RGB format**: `rgb(r,g,b)` (e.g., `rgb(44,48,61)`)
- **RGBA format**: `rgba(r,g,b,a)` (e.g., `rgba(44,48,61,0.8)`)

### File Path Rules
- **Relative paths**: Relative to theme directory
- **Supported formats**: PNG, JPG, JPEG, SVG, ICO
- **Font formats**: TTF, OTF, WOFF, WOFF2

### Validation Rules
1. **Required sections**: [general], [colors], [fonts] must exist
2. **Required keys**: name, title, logo, icon, backgroundcolor, maintextcolor, mainfont
3. **Color validation**: All color values must be valid CSS colors
4. **File validation**: Referenced files should exist in theme directory

## Example Theme File

```ini
[general]
name=MyTheme
title=My Custom Theme
version=1.0.0
author=CloudCoin Developer
description=A beautiful custom theme

[images]
logo=assets/images/logo.png
icon=assets/images/icon.png
backgroundimage=assets/images/background.jpg

[colors]
backgroundcolor=#FFFFFF
maintextcolor=#000000
primarybuttoncolor=#007ACC

[fonts]
mainfont=assets/fonts/Roboto-Regular.ttf
mainfontbold=assets/fonts/Roboto-Bold.ttf

[support]
supportemail=help@example.com
supportpage=https://example.com/help
```

## Theme Directory Structure

```
theme_name/
├── Theme.txt              # Main theme configuration
├── assets/
│   ├── images/           # Image assets
│   │   ├── logo.png
│   │   ├── icons/
│   │   └── backgrounds/
│   └── fonts/            # Font files
│       ├── main-font.ttf
│       └── bold-font.ttf
└── README.md             # Theme documentation
```

## Implementation Notes

### For Theme Loaders
- Parse INI format strictly
- Validate all required fields
- Check file existence for assets
- Provide meaningful error messages
- Support fallback to default values

### For Theme Creators
- Follow naming conventions
- Include all required assets
- Test with different screen sizes
- Provide theme documentation
- Version your themes properly

### Error Handling
- Invalid color formats should fallback to defaults
- Missing image files should use placeholder images
- Missing font files should use system defaults
- Invalid sections should be ignored with warnings

This specification ensures that all CloudCoin applications can consistently load and apply themes while maintaining flexibility for customization.