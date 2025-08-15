# Load Theme Function Prompt

This is used to create a function called `load-theme(theme_path: string)`. This function takes one argument: the file path to a theme directory containing a Theme.txt file.

The primary purpose of this function is to parse and load a theme configuration, validate all settings, resolve asset paths, and return a structured theme object that can be used by applications to apply visual styling and branding.

## Function Requirements

### 1. Theme Directory Validation
A "theme directory" must contain a Theme.txt file and optionally an assets directory with images and fonts.
The function must locate and validate the Theme.txt file within the specified theme directory.
The theme_path parameter should point to a directory, not directly to the Theme.txt file.

### 2. INI File Parsing
The function needs to parse the Theme.txt file using INI format parsing rules.
Support for sections ([general], [colors], [fonts], etc.) and key-value pairs.
Handle comments (lines starting with ; or #) and whitespace trimming.

### 3. Asset Path Resolution
The function must resolve relative asset paths to absolute paths based on the theme directory.
Validate that referenced image and font files exist in the theme assets directory.
Create fallback mechanisms for missing assets.

### 4. Return Value
The function must return a structured theme object containing all parsed configuration data with validated and resolved paths.

## Input
- **theme_path** (string): The absolute or relative path to the theme directory

## Output
(object): A structured theme object containing all theme configuration data

## File Structure
Your code will interact with the following directory structure:

```
theme_path/
├── Theme.txt                    # Main theme configuration file
├── assets/
│   ├── images/                 # Image assets
│   │   ├── CloudCoinLogo.png
│   │   ├── icons/
│   │   │   ├── depositicon.png
│   │   │   └── withdrawicon.png
│   │   └── backgrounds/
│   │       └── bglogo.png
│   └── fonts/                  # Font files
│       ├── Montserrat-Regular.otf
│       └── OpenSans-Regular.ttf
└── README.md                   # Optional theme documentation
```

## Detailed Logic Flow

### 1. Validate Input Parameters
- Check if theme_path exists and is a directory
- Verify Theme.txt file exists within the theme directory
- If validation fails, return error object

### 2. Parse Theme Configuration File
- Open Theme.txt file for reading
- Parse INI format sections and key-value pairs
- Handle comments and whitespace trimming
- Store parsed data in structured format

### 3. Validate Required Sections and Keys
- Ensure required sections exist: [general], [colors], [fonts]
- Validate required keys in [general]: name, title
- Validate required color keys: backgroundcolor, maintextcolor
- Validate required font keys: mainfont

### 4. Process and Validate Colors
- Parse color values (hex, rgb, rgba formats)
- Validate color format correctness
- Convert colors to consistent format (hex)
- Set default values for missing colors

### 5. Resolve Asset Paths
- Convert relative asset paths to absolute paths
- Check existence of referenced image files
- Check existence of referenced font files
- Create fallback paths for missing assets

### 6. Construct Theme Object
- Build structured theme object with all configuration
- Include resolved asset paths
- Add validation status for each asset
- Set fallback values where needed

### 7. Return Theme Object
- Return complete theme object with all processed data
- Include error information for any validation failures

## Theme Object Structure

The function returns a theme object with this structure:

```json
{
  "general": {
    "name": "EthBold",
    "title": "EthBold Wallet",
    "version": "1.0.0",
    "versionoffset": 0,
    "terms": "TermsAndConditions.html",
    "author": "CloudCoin Team",
    "description": "Professional dark theme"
  },
  "images": {
    "logo": "/path/to/theme/assets/images/CloudCoinLogo.png",
    "logotext": "/path/to/theme/assets/images/CloudCoinText.png",
    "backgroundimage": "/path/to/theme/assets/images/bglogo.png",
    "icon": "/path/to/theme/assets/images/CloudCoinLogo.png",
    "depositicon": "/path/to/theme/assets/images/depositicon.png",
    "withdrawicon": "/path/to/theme/assets/images/withdrawicon.png"
  },
  "colors": {
    "backgroundcolor": "#2C303D",
    "headerbackgroundcolor": "#1C1F28",
    "maintextcolor": "#D4D4D4",
    "secondtextcolor": "#65676B",
    "primarybuttoncolor": "#AB0000",
    "errorcolor": "#FF0000"
  },
  "fonts": {
    "mainfont": "/path/to/theme/assets/fonts/Montserrat-Regular.otf",
    "mainfontsemibold": "/path/to/theme/assets/fonts/Montserrat-SemiBold.otf",
    "mainfontbold": "/path/to/theme/assets/fonts/Montserrat-Bold.otf"
  },
  "support": {
    "supportemail": "support@ethbold.com",
    "supportpage": "https://ethbold.com/use.html",
    "supporttime": "9AM to 3AM California time (PST)",
    "supportphone": "+1 (530) 762-1234"
  },
  "validation": {
    "valid": true,
    "errors": [],
    "warnings": ["backgroundimage file not found"],
    "missing_assets": []
  }
}
```

## Example Function Call

```bash
load-theme "/path/to/themes/ethbold"
```

## Color Processing Rules

### Supported Color Formats
- **Hex**: `#RGB`, `#RRGGBB`
- **RGB**: `rgb(r,g,b)`
- **RGBA**: `rgba(r,g,b,a)`
- **Named colors**: `red`, `blue`, `white`, etc.

### Color Validation
- Validate hex format: must start with # and contain valid hex digits
- Validate RGB values: must be integers 0-255
- Validate alpha values: must be float 0.0-1.0
- Convert all valid colors to #RRGGBB format

### Default Color Fallbacks
```json
{
  "backgroundcolor": "#FFFFFF",
  "maintextcolor": "#000000",
  "primarybuttoncolor": "#007ACC",
  "errorcolor": "#FF0000",
  "secondtextcolor": "#666666"
}
```

## Asset Path Resolution Rules

### Image Assets
- Support formats: PNG, JPG, JPEG, SVG, ICO, GIF
- Search order: assets/images/, assets/, theme_root/
- Fallback to default assets if file not found

### Font Assets  
- Support formats: TTF, OTF, WOFF, WOFF2
- Search order: assets/fonts/, assets/, theme_root/
- Fallback to system fonts if file not found

## Error Handling

The function should handle these error conditions:

| Error Condition | Response Action |
|-----------------|-----------------|
| Theme directory doesn't exist | Return error: "Theme directory not found" |
| Theme.txt file missing | Return error: "Theme.txt file not found in theme directory" |
| Invalid INI format | Return error: "Invalid Theme.txt format at line {line_number}" |
| Missing required section | Return error: "Required section [{section}] missing" |
| Missing required key | Return error: "Required key '{key}' missing in section [{section}]" |
| Invalid color format | Set default color and add warning |
| Missing asset file | Use fallback asset and add warning |
| Permission denied | Return error: "Unable to read theme files" |

## Validation Object

Include validation information in the returned theme object:

```json
{
  "validation": {
    "valid": true,
    "errors": [
      "Required key 'name' missing in section [general]"
    ],
    "warnings": [
      "Image file 'backgroundimage.png' not found",
      "Invalid color format '#ZZZZZZ' for backgroundcolor"
    ],
    "missing_assets": [
      "assets/images/backgroundimage.png",
      "assets/fonts/missing-font.ttf"
    ],
    "asset_status": {
      "images_found": 15,
      "images_missing": 2,
      "fonts_found": 3,
      "fonts_missing": 1
    }
  }
}
```

## Integration Notes

- This function provides the foundation for theme application systems
- Results can be cached to improve performance on repeated loads
- Theme objects can be serialized for storage or transmission
- Function is read-only and safe to call multiple times
- Supports hot-reloading by calling function again with same path
- Theme validation follows the specification in theme-file-format.md