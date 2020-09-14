# imq_decomp
Decompression software for IMQ images

## requirements
- Python 3.8.2
- Numpy 1.19.1

The software has been tested on Ubuntu 20.04 LTS

## launch the script
python3 imq_decomp /path/to/source /path/to/destination

## how does it work?
The script will find all IMQ compressed files in /path/to/source and its subfolders. Then it saves uncompressed images in /path/to/destination and it makes all the subfolder of the source. For each image the software creates a text file with .info extension which contains more information about the image.  
