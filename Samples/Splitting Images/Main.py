from split_image import split_image

# Split the image into 2 rows and 2 columns
split_image("1.3.1. original.jpg", 4, 4, should_square=False, should_cleanup=False, output_dir="output_tiles")
