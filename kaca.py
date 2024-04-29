import cv2
import matplotlib.pyplot as plt
import numpy as np

#Masih 12 hasilnya

# Default show images in greyscale
plt.gray()

img = cv2.imread('hitung2.jpg',0)

# noise removal
img = cv2.GaussianBlur(img, (5, 5), 0)
ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_OTSU)
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2) 

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=1)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.4*dist_transform.max(),255,0)

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

# Watershed
img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
markers = cv2.watershed(img_color,markers)
img_color[markers == -1] = [255,0,0]

# Calculate selected count
# Exclude the background (label 1) and regions with size equal to the image size
glass_count = len(np.unique(markers)) - 2  # Subtract 2 for background and image size

# Print the count
print("Selected shape Count:", glass_count)

def plot_image(image, figsize=(18,18)):
    fig, ax = plt.subplots(figsize=(18, 20))
    ax.imshow(image, cmap='gray')
    plt.show()

plot_image(img_color)
