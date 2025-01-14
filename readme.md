# Thumbnail Collage Generator

A Python script that generates collages from thumbnail images, designed to handle both single thumbnail directories and complex directory structures with multiple thumbnail folders.

## Features

- Creates organized collages from thumbnail images
- Handles both single thumbnail directories and nested directory structures
- Automatically calculates optimal grid layout based on image sizes
- Excludes existing collages when regenerating
- Configurable via config.ini file
- Detailed logging and progress information
- Support for multiple image formats (jpg, jpeg, png)

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Clone the repository:
```bash
git clone https://github.com/yourusername/thumbnail-collage-generator.git
cd thumbnail-collage-generator
```

3. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

4. Install required dependencies:
```bash
pip install pillow
```

## Usage

The script can handle two common directory structures:

### Structure 1: Single Thumbs Directory
```
parent_directory/
└── thumbs/
    ├── thumb1.jpg
    ├── thumb2.jpg
    └── thumb3.jpg
```

Command:
```bash
python image-collage.py /path/to/parent_directory
```

### Structure 2: Multiple Subdirectories with Thumbs
```
parent_directory/
├── bundle1/
│   └── thumbs/
│       ├── thumb1.jpg
│       └── thumb2.jpg
├── bundle2/
│   └── thumbs/
│       ├── thumb3.jpg
│       └── thumb4.jpg
└── bundle3/
    └── thumbs/
        ├── thumb5.jpg
        └── thumb6.jpg
```

Command:
```bash
python image-collage.py /path/to/parent_directory
```

### Command Line Options

```bash
python image-collage.py [directory] [options]

Options:
  -size SIZE    Target size for the collage (default: 2000)
  -c CONFIG     Path to config file (default: config.ini)
  -h, --help    Show help message
```

## Configuration

The script creates a default `config.ini` file on first run with these settings:

```ini
[DEFAULT]
supported_formats = .jpg,.jpeg,.png
jpeg_quality = 85
skip_errors = True
```

You can modify these settings:
- `supported_formats`: List of supported image file extensions
- `jpeg_quality`: Output JPEG quality (1-100)
- `skip_errors`: Whether to continue processing if an error occurs with a single image

## Output

- Collages are saved in the same directory as the source thumbnails
- Files are named `collage_1.jpg`, `collage_2.jpg`, etc.
- Each run automatically excludes existing collages from being reprocessed

## Example Output

```bash
Processing subdirectory: bundle1
Found 50 images in bundle1/thumbs
Created 2 collage(s) for bundle1:
- /path/to/bundle1/thumbs/collage_1.jpg
- /path/to/bundle1/thumbs/collage_2.jpg

Processing subdirectory: bundle2
Found 30 images in bundle2/thumbs
Created 1 collage(s) for bundle2:
- /path/to/bundle2/thumbs/collage_1.jpg
```

## Error Handling

- The script includes detailed error logging
- Errors with individual images won't stop the entire process
- Clear feedback about missing directories or files
- Validation of image formats and directory structures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Created for efficient thumbnail collage generation
- Uses Python's Pillow library for image processing
- Designed for flexibility with different directory structures
- Thanks to all contributors and users