# Validate Theme Function Prompt

This is used to create a function called `validate-theme(theme_path: string)`. This function takes one argument: the file path to a theme directory containing a Theme.txt file.

The primary purpose of this function is to thoroughly validate a theme configuration for correctness, completeness, and compatibility before it can be loaded and applied by applications. It checks file format, required sections, asset availability, and provides detailed validation reports.

## Function Requirements

### 1. Theme Directory Structure Validation
The function must verify that the theme directory contains the required Theme.txt file.
Check for proper directory structure including assets subdirectories.
Validate that all referenced asset files exist and are accessible.

### 2. Theme Configuration Format Validation
Parse and validate the INI format of the Theme.txt file.
Verify all required sections and keys are present.
Check data types and formats for all configuration values.

### 3. Asset Validation
Validate that all referenced image files exist and are in supported formats.
Check that font files exist and are in supported formats.
Verify file permissions and accessibility.

### 4. Return Value
The function must return a comprehensive validation report indicating all issues found, missing requirements, and overall validation status.

## Input
- **theme_path** (string): The absolute or relative path to the theme directory

## Output
(object): Detailed validation report with pass/fail status and specific issues

## File Structure
Your code will interact with the following directory structure:

```
theme_path/
├── Theme.txt                    # Main theme configuration file (REQUIRED)
├── assets/                     # Assets directory (OPTIONAL)
│   ├── images/                 # Image assets (OPTIONAL)
│   │   ├── CloudCoinLogo.png
│   │   ├── icons/
│   │   └── backgrounds/
│   └── fonts/                  # Font files (OPTIONAL)
│       ├── Montserrat-Regular.otf
│       └── OpenSans-Regular.ttf
└── README.md                   # Theme documentation (OPTIONAL)
```

## Detailed Logic Flow

### 1. Validate Input Parameters
- Check if theme_path exists and is accessible
- Verify theme_path points to a directory (not a file)
- Check read permissions for the directory

### 2. Validate Theme.txt File
- Verify Theme.txt file exists in the theme directory
- Check file is readable and not empty
- Validate file encoding (should be UTF-8 compatible)

### 3. Parse and Validate INI Format
- Parse the Theme.txt file using INI format rules
- Check for syntax errors in the INI format
- Validate section headers and key-value pairs
- Handle comments and whitespace correctly

### 4. Validate Required Sections
- Check for required sections: [general], [colors], [fonts]
- Validate optional sections: [images], [support]
- Report missing required sections

### 5. Validate Required Keys
- In [general] section: name, title (required)
- In [colors] section: backgroundcolor, maintextcolor (required)
- In [fonts] section: mainfont (required)
- Report missing required keys

### 6. Validate Data Types and Formats
- Validate all color values (hex, rgb, rgba formats)
- Check string values for proper format
- Validate numeric values where applicable
- Check boolean values if present

### 7. Validate Asset References
- Check all image file references in [images] section
- Verify all font file references in [fonts] section
- Validate file paths are relative to theme directory
- Check file extensions are supported

### 8. Validate Asset Files
- Verify referenced files actually exist
- Check file permissions and accessibility
- Validate file formats (PNG, JPG for images; TTF, OTF for fonts)
- Check file sizes are reasonable

### 9. Perform Compatibility Checks
- Validate theme follows theme-file-format.md specification
- Check for deprecated or unsupported features
- Validate color contrast for accessibility
- Check font licensing compatibility if possible

### 10. Generate Validation Report
- Compile all validation results
- Categorize issues by severity (errors, warnings, info)
- Provide specific recommendations for fixes
- Calculate overall validation score

## Validation Categories

### Critical Errors (Must Fix)
- Missing Theme.txt file
- Invalid INI format syntax
- Missing required sections
- Missing required keys
- Invalid color formats
- Referenced files don't exist

### Warnings (Should Fix)
- Missing optional but recommended sections
- Missing optional assets
- Poor color contrast
- Large file sizes
- Deprecated features

### Information (Nice to Have)
- Missing optional keys
- Suggestions for improvements
- Performance recommendations
- Accessibility suggestions

## Color Validation Rules

### Supported Color Formats
```javascript
// Valid hex colors
#RGB       // e.g., #F00
#RRGGBB    // e.g., #FF0000

// Valid RGB colors  
rgb(r,g,b)           // e.g., rgb(255,0,0)
rgba(r,g,b,a)        // e.g., rgba(255,0,0,0.5)

// Valid named colors
red, blue, white, black, etc.
```

### Color Validation Logic
```javascript
function validateColor(colorValue) {
    // Check hex format
    if (/^#([0-9A-F]{3}|[0-9A-F]{6})$/i.test(colorValue)) {
        return { valid: true, format: 'hex' };
    }
    
    // Check RGB format
    if (/^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$/i.test(colorValue)) {
        return { valid: true, format: 'rgb' };
    }
    
    // Check RGBA format
    if (/^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$/i.test(colorValue)) {
        return { valid: true, format: 'rgba' };
    }
    
    return { valid: false, error: 'Invalid color format' };
}
```

## Asset Validation Rules

### Supported Image Formats
- **PNG** (preferred for icons and logos)
- **JPG/JPEG** (acceptable for photos and backgrounds)
- **SVG** (acceptable for scalable graphics)
- **ICO** (acceptable for application icons)
- **GIF** (acceptable but not recommended)

### Supported Font Formats
- **TTF** (TrueType Font - widely supported)
- **OTF** (OpenType Font - preferred)
- **WOFF** (Web Open Font Format)
- **WOFF2** (Web Open Font Format 2.0)

### File Size Recommendations
- **Images**: < 5MB per file, < 50MB total
- **Fonts**: < 2MB per file, < 20MB total
- **Total theme**: < 100MB

## Validation Response Object

```json
{
  "valid": false,
  "overall_score": 75,
  "theme_name": "EthBold",
  "validation_timestamp": "2025-01-15T10:30:00Z",
  "summary": {
    "total_checks": 45,
    "passed": 35,
    "warnings": 8,
    "errors": 2
  },
  "sections": {
    "general": {
      "valid": true,
      "required_keys": ["name", "title"],
      "missing_keys": [],
      "warnings": ["version not specified"]
    },
    "colors": {
      "valid": false,
      "required_keys": ["backgroundcolor", "maintextcolor"],
      "missing_keys": [],
      "errors": ["Invalid color format: '#ZZZZZZ'"],
      "warnings": ["Low contrast between text and background"]
    },
    "fonts": {
      "valid": true,
      "required_keys": ["mainfont"],
      "missing_keys": [],
      "warnings": ["Font file size is large: 3.2MB"]
    },
    "images": {
      "valid": true,
      "total_references": 25,
      "found": 23,
      "missing": 2,
      "errors": [],
      "warnings": ["backgroundimage.png not found"]
    }
  },
  "assets": {
    "images": {
      "total_size": "15.2MB",
      "count": 23,
      "missing_files": [
        "assets/images/backgroundimage.png",
        "assets/images/missing-icon.png"
      ]
    },
    "fonts": {
      "total_size": "8.5MB", 
      "count": 3,
      "missing_files": []
    }
  },
  "recommendations": [
    "Fix invalid color format in backgroundcolor",
    "Add missing image files or remove references",
    "Consider optimizing font file sizes",
    "Improve color contrast for accessibility"
  ],
  "compatibility": {
    "spec_version": "1.0.0",
    "deprecated_features": [],
    "platform_support": {
      "desktop": true,
      "web": true,
      "mobile": true
    }
  }
}
```

## Example Function Call

```bash
validate-theme "/path/to/themes/ethbold"
```

## Error Response Examples

### Missing Theme File
```json
{
  "valid": false,
  "error": "THEME_FILE_NOT_FOUND",
  "message": "Theme.txt file not found in directory '/path/to/themes/ethbold'",
  "validation_timestamp": "2025-01-15T10:30:00Z"
}
```

### Invalid Directory
```json
{
  "valid": false,
  "error": "INVALID_THEME_DIRECTORY", 
  "message": "Specified path is not a directory or does not exist",
  "validation_timestamp": "2025-01-15T10:30:00Z"
}
```

### INI Format Error
```json
{
  "valid": false,
  "error": "INVALID_INI_FORMAT",
  "message": "Invalid INI format at line 15: missing section header",
  "validation_timestamp": "2025-01-15T10:30:00Z"
}
```

## Validation Checklist

### ✅ **Required Validations**
- [ ] Theme.txt file exists
- [ ] Valid INI format
- [ ] Required sections present
- [ ] Required keys present
- [ ] Valid color formats
- [ ] Referenced assets exist

### ⚠️ **Recommended Validations**
- [ ] Optional sections present
- [ ] Good color contrast
- [ ] Reasonable file sizes
- [ ] Supported file formats
- [ ] No deprecated features

### ℹ️ **Optional Validations**
- [ ] Theme documentation present
- [ ] Consistent naming conventions
- [ ] Performance optimization
- [ ] Accessibility compliance

## Integration Notes

- This function should be called before load-theme to catch issues early
- Can be integrated into theme development tools for real-time validation
- Provides foundation for theme quality assurance and testing
- Supports automated theme validation in CI/CD pipelines
- Can be used to validate themes before publishing or distribution
- Works in conjunction with load-theme and apply-theme functions