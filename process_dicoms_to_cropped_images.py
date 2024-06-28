import os
import pydicom
import numpy as np
from PIL import Image
import logging
import gc

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check memory and system status
def check_system_status():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    virtual_mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    logging.info(f"Process memory usage: {mem_info.rss / 1024 ** 2:.2f} MB")
    logging.info(f"Total memory: {virtual_mem.total / 1024 ** 2:.2f} MB")
    logging.info(f"Available memory: {virtual_mem.available / 1024 ** 2:.2f} MB")
    logging.info(f"Used memory: {virtual_mem.used / 1024 ** 2:.2f} MB")
    logging.info(f"Swap usage: {swap.used / 1024 ** 2:.2f} MB")

# Function to normalize pixel data in chunks
def normalize_pixel_data(pixel_array):
    min_val = pixel_array.min()
    max_val = pixel_array.max()
    logging.info(f"Min pixel value: {min_val}, Max pixel value: {max_val}")

    # Normalize pixel array in chunks to avoid high memory usage
    chunk_size = 1024 * 1024  # Adjust chunk size as needed
    normalized_array = np.empty(pixel_array.shape, dtype=np.uint8)

    for start in range(0, pixel_array.size, chunk_size):
        end = start + chunk_size
        chunk = pixel_array.flat[start:end]
        normalized_array.flat[start:end] = (255.0 / max_val * (chunk - min_val)).astype(np.uint8)
        check_system_status()
        gc.collect()  # Explicitly free memory

    return normalized_array

# Function to crop the central part of an image
def crop_center(image, crop_width, crop_height):
    img_width, img_height = image.size
    logging.info(f"Image size: {img_width}x{img_height}")

    left = (img_width - crop_width) // 2
    top = (img_height - crop_height) // 2
    right = (img_width + crop_width) // 2
    bottom = (img_height + crop_height) // 2

    return image.crop((left, top, right, bottom))

# Function to process a single DICOM file and extract, normalize, and crop frames
def process_dicom_file(dicom_path, output_base_folder, crop_width=400, crop_height=400):
    try:
        logging.info(f"Reading DICOM file: {dicom_path}")
        dicom = pydicom.dcmread(dicom_path)
        check_system_status()

        logging.info(f"Extracting pixel data")
        try:
            pixel_array = dicom.pixel_array
            logging.info(f"Pixel array shape: {pixel_array.shape}")
        except AttributeError as e:
            logging.error(f"Error extracting pixel data from {dicom_path}: {e}")
            return

        check_system_status()

        logging.info(f"Normalizing pixel data")
        pixel_array_normalized = normalize_pixel_data(pixel_array)
        check_system_status()

        # Create output directory for the DICOM file
        dicom_name = os.path.basename(dicom_path)
        dicom_output_folder = os.path.join(output_base_folder, dicom_name)
        if not os.path.exists(dicom_output_folder):
            os.makedirs(dicom_output_folder)

        # Process each frame in the DICOM file
        if len(pixel_array_normalized.shape) == 3:
            for i in range(pixel_array_normalized.shape[0]):
                frame = pixel_array_normalized[i]
                image = Image.fromarray(frame)
                cropped_image = crop_center(image, crop_width, crop_height)

                output_path = os.path.join(dicom_output_folder, f"{i:04d}.png")
                cropped_image.save(output_path)
                logging.info(f"Saved cropped frame to: {output_path}")
        else:
            logging.error(f"Unexpected pixel array shape: {pixel_array_normalized.shape}")
            return

        check_system_status()

    except Exception as e:
        logging.error(f"Could not process {dicom_path}: {e}")

# Function to process all DICOM files in a directory
def process_all_dicoms(input_folder, output_base_folder, crop_width=400, crop_height=400):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.dcm') or file.lower() == "dicomdir":
                continue
            process_dicom_file(file_path, output_base_folder, crop_width, crop_height)

# Base directory containing the DICOM files
input_folder = "."
output_base_folder = "."

# Process all DICOM files
process_all_dicoms(input_folder, output_base_folder)


# Process all DICOM files
process_all_dicoms(input_folder, output_base_folder)

