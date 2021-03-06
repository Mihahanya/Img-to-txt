import numpy as np
from PIL import Image
import sys, os
from numba import njit

path_to_img = sys.argv[1] if len(sys.argv) != 1 else input('Path to image: ')
width = int(input('Width: '))

print('Processing...')

PW = 8
PH = 16

img = Image.open(path_to_img)
img = img.resize((width*PW, int(img.size[1]/img.size[0]*width / (18/8)) * PH))
pix = np.asarray(img.convert('L'))

h = pix.shape[0]
w = pix.shape[1]

tones = []
p_dir = 's/'

for i in range(95):
    p = np.asarray(Image.open(p_dir + str(i) + '.png').convert('L'))

    tones.append(p.sum() / PW / PH)

tones -= min(tones)
tones *= 255/max(tones)
tones = np.array(tones)

gradient = '1234567890~`!@#$%^&*()-=_+{}[]:";\'<>?,./\\|qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM '

@njit
def check_pattern(pat):
    ps = pat.sum() / PW / PH
    it = 0
    min_d = 256
    for i in range(len(tones)):
        d = abs(tones[i] - ps)
        if d < min_d:
            min_d = d
            it = i
    return it

f = open('res.txt', 'w')

for y in range(PH, h, PH):
    for x in range(PW, w, PW):
        part = pix[y-PH:y, x-PW:x]
        r = check_pattern(part)
        f.write(gradient[r])
    f.write('\n')
    print(round(y / h * 100, 1))

f.close()
