import os
import argparse
import configparser
from PIL import Image
import math
from typing import List, Tuple
import logging

class CollageGenerator:
    def __init__(self, config_path: str = "config.ini"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("CollageGenerator")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_config(self, config_path: str) -> configparser.ConfigParser:
        config = configparser.ConfigParser()
        default_config = {
            'supported_formats': '.jpg,.jpeg,.png',
            'jpeg_quality': '85',
            'skip_errors': 'True'
        }
        
        config['DEFAULT'] = default_config
        
        if os.path.exists(config_path):
            config.read(config_path)
        else:
            with open(config_path, 'w') as config_file:
                config.write(config_file)
        
        for key, value in default_config.items():
            if key not in config['DEFAULT']:
                config['DEFAULT'][key] = value
        
        return config

    def get_image_files(self, directory: str) -> List[str]:
        """Get all image files from a directory, excluding existing collages"""
        supported_formats = self.config['DEFAULT']['supported_formats'].split(',')
        image_files = []

        self.logger.info(f"Scanning directory: {directory}")
        self.logger.info(f"Supported formats: {supported_formats}")

        # Only look in the specified directory
        files = [f for f in os.listdir(directory) 
                if os.path.isfile(os.path.join(directory, f))]
        
        for file in files:
            # Skip files that start with 'collage_'
            if file.lower().startswith('collage_'):
                self.logger.debug(f"Skipping existing collage: {file}")
                continue
                
            if any(file.lower().endswith(fmt) for fmt in supported_formats):
                full_path = os.path.join(directory, file)
                image_files.append(full_path)
                self.logger.debug(f"Found image: {full_path}")

        self.logger.info(f"Found {len(image_files)} images (excluding existing collages)")
        return sorted(image_files)

    def calculate_grid_size(self, num_images: int, target_size: int) -> Tuple[int, int]:
        grid_size = math.ceil(math.sqrt(num_images))
        return grid_size, grid_size

    def create_collages(self, image_files: List[str], target_size: int) -> List[str]:
        if not image_files:
            self.logger.error("No image files found")
            return []

        self.logger.info(f"Processing {len(image_files)} images")
        
        # Check if target size is reasonable
        if target_size < 100:  # arbitrary minimum size
            self.logger.warning(f"Target size {target_size} is too small, using 2000 as default")
            target_size = 2000

        sample_image = Image.open(image_files[0])
        thumb_size = sample_image.size
        sample_image.close()

        # Calculate images per row, ensuring at least 1
        images_per_row = max(1, target_size // thumb_size[0])
        # Calculate images per collage, ensuring at least 1
        images_per_collage = max(1, images_per_row * images_per_row)
        
        self.logger.info(f"Thumbnail size: {thumb_size}")
        self.logger.info(f"Images per row: {images_per_row}")
        self.logger.info(f"Images per collage: {images_per_collage}")
        
        # Use the input directory as the output directory
        output_dir = os.path.dirname(image_files[0])
        collage_paths = []
        
        for chunk_idx, i in enumerate(range(0, len(image_files), images_per_collage)):
            chunk_files = image_files[i:i + images_per_collage]
            rows, cols = self.calculate_grid_size(len(chunk_files), target_size)
            
            collage = Image.new('RGB', (cols * thumb_size[0], rows * thumb_size[1]), 'white')
            
            for idx, img_path in enumerate(chunk_files):
                try:
                    row = idx // cols
                    col = idx % cols
                    
                    with Image.open(img_path) as img:
                        img = img.convert('RGB')
                        collage.paste(img, (col * thumb_size[0], row * thumb_size[1]))
                        
                except Exception as e:
                    self.logger.error(f"Error processing {img_path}: {str(e)}")
                    if not self.config['DEFAULT'].getboolean('skip_errors'):
                        raise

            output_path = os.path.join(output_dir, f'collage_{chunk_idx + 1}.jpg')
            collage.save(output_path, quality=self.config['DEFAULT'].getint('jpeg_quality'))
            collage_paths.append(output_path)
            
            self.logger.info(f"Created collage {chunk_idx + 1} with {len(chunk_files)} images")

        return collage_paths

def main():
    parser = argparse.ArgumentParser(description='Create image collages from thumbnails')
    parser.add_argument('directory', help='Directory containing image files')
    parser.add_argument('-size', type=int, default=2000,
                        help='Target size for the collage (default: 2000)')
    parser.add_argument('-s', '--subdirs', action='store_true',
                        help='Include subdirectories')
    parser.add_argument('-c', '--config', default='config.ini',
                        help='Path to config file (default: config.ini)')
    
    args = parser.parse_args()
    generator = CollageGenerator(args.config)
    
    # First check if there's a thumbs directory directly in the root
    root_thumbs = os.path.join(args.directory, 'thumbs')
    if os.path.isdir(root_thumbs):
        print("\nProcessing root thumbs directory")
        image_files = generator.get_image_files(root_thumbs)
        
        if image_files:
            print(f"Found {len(image_files)} images in root thumbs directory")
            collage_paths = generator.create_collages(image_files, args.size)
            
            if collage_paths:
                print(f"Created {len(collage_paths)} collage(s):")
                for path in collage_paths:
                    print(f"- {path}")
        return

    # If no root thumbs directory, process subdirectories
    subdirs = [d for d in os.listdir(args.directory) 
              if os.path.isdir(os.path.join(args.directory, d))]
    
    if not subdirs:
        print("No subdirectories found in the specified directory")
        return
        
    # Process each subdirectory separately
    for subdir in subdirs:
        subdir_path = os.path.join(args.directory, subdir)
        print(f"\nProcessing subdirectory: {subdir}")
        
        # Get images from the thumbs directory within this subdirectory
        thumbs_dir = os.path.join(subdir_path, 'thumbs')
        if not os.path.isdir(thumbs_dir):
            print(f"No thumbs directory found in {subdir}")
            continue
            
        image_files = generator.get_image_files(thumbs_dir)
        
        if not image_files:
            print(f"No images found in {thumbs_dir}")
            continue
        
        print(f"Found {len(image_files)} images in {subdir}/thumbs")
        collage_paths = generator.create_collages(image_files, args.size)
        
        if collage_paths:
            print(f"Created {len(collage_paths)} collage(s) for {subdir}:")
            for path in collage_paths:
                print(f"- {path}")

if __name__ == "__main__":
    main()