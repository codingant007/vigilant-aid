import sys
import re
from sets import Set
from PIL import Image
import numpy as np

WINDOW_SIZE = 32	# Size of the sample
TILE_DIMENSION	= 8	# Divide the image into tiles with no intersection
HALF_WINDOW_SIZE = int(TILE_DIMENSION/2)

image_url = sys.argv[1]
KEY_URL = sys.argv[2]

image = Image.open(image_url)
f = open(KEY_URL)

no_of_ip = int(f.readline().split()[0])

def get_sample_asarray(im,x,y):
	im_cropped = im.crop((x-HALF_WINDOW_SIZE,y-HALF_WINDOW_SIZE,x+HALF_WINDOW_SIZE,y+HALF_WINDOW_SIZE))
	im_array = np.array(im_cropped.getdata())
	return im_array

# Return the coordinates of the tile to which a point belongs to
def get_tile_coordinates(x,y):
	return (get_nearest_coordinate(x),get_nearest_coordinate(y))

def get_nearest_coordinate(a):
	threshold = int(a/8) + 0.5
	if(float(a)/8 < threshold):
		return int(a/8) * 8
	else:
		return (int(a/8) + 1)*8

def save_sample(image,x,y,sample_no):
	sample_array = get_sample_asarray(image,x,y)
	f = open(KEY_URL.split('.')[0]+ '-' + str(sample_no) +'.sample','w')
	# Write each pixel triplet 
	for sample in sample_array:
		pixel_string = ''
		# if image is greyscale
		if isinstance(sample, np.int64) :
			pixel_string = ' '.join([str(sample),str(sample),str(sample)]) + '\n'
		else:
			pixel_string = ' '.join(str(e) for e in sample) + '\n'
		f.write(pixel_string)
	# Write class and group
	f.write(KEY_URL.split('.')[0].split('/')[-1])
	f.write(" ")
	f.write(KEY_URL.split('/')[-2])
	f.write('\n')
	f.close()


used_tiles = Set()

i=0
for line in f.readlines():
	m = re.match(r'([0-9]*\.[0-9]*) ([0-9]*\.[0-9]*).*\n',line)
	if(m):
		#print m.group(1),m.group(2)
		x = int(float(m.group(1)))
		y = int(float(m.group(2)))
		x,y = get_tile_coordinates(x,y)
		if (x,y) not in used_tiles:
			i=i+1
			save_sample(image,x,y,i)
			# Add x,y to used tiles
			used_tiles.add((x,y))
