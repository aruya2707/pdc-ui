import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2


def grayscale():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]
    new_arr = r.astype(int) + g.astype(int) + b.astype(int)
    new_arr = (new_arr/3).astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True

# tidak ada perubahan unutk zoom karna ada batasan
def zoomin():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    new_size = ((img_arr.shape[0] * 2),
                (img_arr.shape[1] * 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    new_arr.setflags(write=1)

    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]

    new_r = []
    new_g = []
    new_b = []

    for row in range(len(r)):
        temp_r = []
        temp_g = []
        temp_b = []
        for i in r[row]:
            temp_r.extend([i, i])
        for j in g[row]:
            temp_g.extend([j, j])
        for k in b[row]:
            temp_b.extend([k, k])
        for _ in (0, 1):
            new_r.append(temp_r)
            new_g.append(temp_g)
            new_b.append(temp_b)

    for i in range(len(new_arr)):
        for j in range(len(new_arr[i])):
            new_arr[i, j, 0] = new_r[i][j]
            new_arr[i, j, 1] = new_g[i][j]
            new_arr[i, j, 2] = new_b[i][j]

    new_arr = new_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def zoomout():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    x, y = img.size
    new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
    r = [0, 0, 0, 0]
    g = [0, 0, 0, 0]
    b = [0, 0, 0, 0]

    for i in range(0, int(x/2)):
        for j in range(0, int(y/2)):
            r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
            r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
            r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
            r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
            new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
    new_arr = np.uint8(new_arr)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
    g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
    b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
    g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
    b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    h_img, w_img, _ = img.shape
    out = np.zeros((h_img-2, w_img-2), dtype=np.float64)
    new_img = np.zeros((h_img-2, w_img-2, 3))
    if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
        array = img[:, :, 0]
        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(array[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)
        out_ = np.clip(out, 0, 255)
        for channel in range(3):
            new_img[:, :, channel] = out_
    else:
        for channel in range(3):
            array = img[:, :, channel]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            new_img[:, :, channel] = out_
    new_img = np.uint8(new_img)
    return new_img


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    
    # Since edge detection typically results in a grayscale image,
    # we convert it to uint8 format for saving
    new_arr = new_arr.astype('uint8')
    
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")



def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=np.int64)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)

    if is_grey_scale(img_path):
        grayscale_values = img_arr.flatten()
        data_gray = Counter(grayscale_values)
        plt.bar(list(data_gray.keys()), data_gray.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        
        data_rgb = [data_r, data_g, data_b]
        colors = ['red', 'green', 'blue']
        
        for data, color in zip(data_rgb, colors):
            plt.bar(list(data.keys()), data.values(), color=color)
            plt.savefig(f'static/img/{color}_histogram.jpg', dpi=300)
            plt.clf()


# to make a histogram (count distribution frequency)
def df(img):  
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    condition = np.logical_and(np.greater_equal(img_arr, lower_thres),
                               np.less_equal(img_arr, upper_thres))
    print(lower_thres, upper_thres)
    img_cpy = img_arr.copy() 
    # img_arr.flags.writeable =  1
    img_cpy[condition] = 255
    new_img = Image.fromarray(img_cpy)
    new_img.save("static/img/img_now.jpg")

def dilasi():
    img = cv2.imread('static/img/img_now.jpg')
    kernel = np.ones((3,3), np.uint8)
    dilated_img = cv2.dilate(img, kernel, iterations=1)
    new_img = Image.fromarray(dilated_img)
    new_img.save('static/img/img_now.jpg')

def erosi():
    img = cv2.imread('static/img/img_now.jpg')
    kernel = np.ones((3,3), np.uint8)
    erode_img = cv2.erode(img, kernel, iterations=1)
    new_img = Image.fromarray(erode_img)
    new_img.save('static/img/img_now.jpg')

def opening():
    img = cv2.imread('static/img/img_now.jpg')
    kernel = np.ones((3,3), np.uint8)
    erode_img = cv2.erode(img, kernel, iterations=1)
    dilated_img = cv2.dilate(erode_img, kernel, iterations=1)
    new_img = Image.fromarray(dilated_img)
    new_img.save('static/img/img_now.jpg')

def closing():
    img = cv2.imread('static/img/img_now.jpg')
    kernel = np.ones((3,3), np.uint8)
    dilated_img = cv2.dilate(img, kernel, iterations=1)
    erode_img = cv2.erode(dilated_img, kernel, iterations=1)
    new_img = Image.fromarray(erode_img)
    new_img.save('static/img/img_now.jpg')

def count_object1():
    img = cv2.imread('static/img/img_now.jpg', 0)

    # noise removal
    img = cv2.GaussianBlur(img, (5, 5), 0)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=1)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.4 * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    # Watershed
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    markers = cv2.watershed(img_color, markers)
    img_color[markers == -1] = [255, 0, 0]

    # Calculate selected count
    # Exclude the background (label 1) and regions with size equal to the image size
    shape_count = len(np.unique(markers)) - 2  # Subtract 2 for background and image size

    new_img = Image.fromarray(img_color)
    new_img.save('static/img/img_now.jpg')
    
    message = "jumlah objek : " + str(shape_count)
    return message

def extract_freeman_chain_code(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Temukan kontur dalam citra
    contour = max(contours, key=cv2.contourArea)
    freeman_chain_code = []
    
    for i in range(1, len(contour)):
        dx = contour[i][0][0] - contour[i-1][0][0]
        dy = contour[i][0][1] - contour[i-1][0][1]
        code = 0
        # Hitung arah Freeman Chain Code
        if dx == 1 and dy == 0:
            code = 0
        elif dx == 1 and dy == -1:
            code = 1
        elif dx == 0 and dy == -1:
            code = 2
        elif dx == -1 and dy == -1:
            code = 3
        elif dx == -1 and dy == 0:
            code = 4
        elif dx == -1 and dy == 1:
            code = 5
        elif dx == 0 and dy == 1:
            code = 6
        elif dx == 1 and dy == 1:
            code = 7
        
        freeman_chain_code.append(code)   # Tambahkan ke Freeman Chain Code
    np_freeman_chain_code = np.array(freeman_chain_code)
    return np_freeman_chain_code

def add_knowledge():
    angka = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    array_angka = []
    for i in range(len(angka)):
        freeman_code = extract_freeman_chain_code('static/knowledge/' + angka[i] + '.png')
        array_angka.append(freeman_code)
        print("Freeman Chain Code " + str(i) + ':', freeman_code)
    return array_angka

def deteksi_angka(image_path, knowledge):    
    np_freeman_chain_code = extract_freeman_chain_code(image_path)
    for i in range(len(knowledge)):
        if(np.array_equal(np_freeman_chain_code, knowledge[i])):
            print('angka terdeteksi: ' + str(i))
            return str(i)
        
def merge_image(image_path1, image_path2):
    gambar1 = Image.open(image_path1)
    gambar2 = Image.open(image_path2)

    # Periksa ukuran gambar
    lebar_gambar1, tinggi_gambar1 = gambar1.size
    lebar_gambar2, tinggi_gambar2 = gambar2.size

    # Hitung lebar dan tinggi baru untuk gambar gabungan
    lebar_gabungan = lebar_gambar1 + lebar_gambar2
    tinggi_gabungan = max(tinggi_gambar1, tinggi_gambar2)

    # Buat gambar baru untuk gabungan
    gabungan = Image.new('RGB', (lebar_gabungan, tinggi_gabungan))

    # Tempelkan gambar pertama
    gabungan.paste(gambar1, (0, 0))

    # Tempelkan gambar kedua
    gabungan.paste(gambar2, (lebar_gambar1, 0))

    # Simpan gambar gabungan
    gabungan.save('static/img/img_now.jpg')

def emoji_knowledge():
    emojis = [
        "blush", "disappointed_relieved", "expressionless", "face_with_raised_eyebrow",
        "face_with_rolling_eyes", "grin", "grinning", "heart_eyes", "hugging_face",
        "hushed", "joy", "kissing", "kissing_closed_eyes", "kissing_heart",
        "kissing_smiling_eyes", "laughing", "neutral_face", "no_mouth", "open_mouth",
        "persevere", "relaxed", "rolling_on_the_floor_laughing", "sleeping", "sleepy",
        "slightly_smiling_face", "smile", "smiley", "smirk", "star-struck", "sunglasses",
        "sweat_smile", "thinking_face", "tired_face", "wink", "yum", "zipper_mouth_face"
    ]

    emoji_dict = {}
    for i in range(len(emojis)):
        freeman_code = extract_freeman_chain_code('static/emoji/'+ emojis[i] + '.png')
        emoji_dict[emojis[i]] = freeman_code
        print("Freeman Chain Code " + emojis[i] + ':', freeman_code)
    return emoji_dict

def deteksi_emoji(image_path, knowledge):
    np_freeman_chain_code = extract_freeman_chain_code(image_path)
    print('bisa')
    for emoji_name, chaincode in knowledge.items():
        if(np.array_equal(np_freeman_chain_code, chaincode)):
            print('emoji terdeteksi: ' + emoji_name)
            return emoji_name
        
