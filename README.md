# DICOM Frame Extraction and Cropping

This project processes DICOM files to extract all frames, normalize them, crop the central 430x430 pixels of each frame, and save these cropped images in separate directories named after the original DICOM files. The cropping process is intended to remove the text from the original images while keeping the image ratio and relevant information. You can adjust the center size in the code.

## Setup

To set up the project environment, follow these steps:

1. **Create a conda environment named `ultrasound` with Python 3.9**:
    ```bash
    conda create -n ultrasound python=3.9
    ```

2. **Activate the environment**:
    ```bash
    conda activate ultrasound
    ```

3. **Install the required libraries from `requirements.txt`**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Script

To run the script and process the DICOM files:

1. **Place the DICOM files in the current directory**.
2. **Run the script**:
    ```bash
    python process_dicoms_to_cropped_images.py
    ```

This script will process each DICOM file in the current directory, extract all frames, normalize and crop the central 400x400 pixels, and save the cropped images in a new directory named after the original DICOM file.

## Example

In the `assets` folder, you will find examples of a complete image and a cropped image:

- **assets/complete_image.png**: This is an example of a complete frame extracted from a DICOM file.
- **assets/cropped_image.png**: This is the cropped central 430x430 pixels of the complete frame.

These images illustrate the processing performed by the script.

## Directory Structure

After running the script, your directory structure will look like this:

```
.
├── PD4BU7WZ
│ ├── 0000.png
│ ├── 0001.png
│ ├── ...
│ └── 0059.png
├── SCDGHPL1
│ ├── 0000.png
│ ├── 0001.png
│ ├── ...
│ └── 0059.png
├── process_dicoms_to_cropped_images.py
├── requirements.txt
└── assets
├── complete_image.png
└── cropped_image.png
```

Each DICOM file will have its own directory with the cropped frames saved as PNG images.

## Notes

- Ensure that the DICOM files are in the current directory when running the script.
- The script handles large files efficiently by processing pixel data in chunks and managing memory usage.

For any issues or questions, please contact the project maintainer.
