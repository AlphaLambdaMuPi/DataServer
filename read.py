import numpy as np
import scipy
from scipy import stats
import json
import base64
import matplotlib.pyplot as plt
import cv2

f = list(open('data/Nexus 5-3.txt'))
f = [json.loads(x.strip('\n')) for x in f]

acc = []
tm = []

pic = {}

for d in f:
    if d['type'] == 'accel':
        tm.append(d['time'])
        acc.append(json.loads(d['data']))
    elif d['type'] == 'camera':
        tim = d['time']
        if tim not in pic:
            pic[tim] = ''
        pic[tim] += d['data'].replace('\n', '')

cnt = 0
for i in sorted(pic.keys()):
    cnt += 1
    pic[i] = base64.b64decode(bytes(pic[i], 'ascii'))
    print(len(pic[i]))

    height = 480
    width = 640

    p = list(pic[i])
    p = np.array(p).reshape(height*1.5, width).astype('uint8')
    p = cv2.cvtColor(p, cv2.COLOR_YUV2RGBA_NV21)
    p = p[:,:,[2,1,0,3]]
    p = p.transpose((1, 0, 2))
    p = p[:,::-1,:]
    # cv2.imshow('a', p)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite('libviso2/img/b{:03d}.jpg'.format(cnt), p)


acc = np.array(acc)
tm = np.array(tm) / 1E9
tm -= tm[0]

def stat(x):
    mean = np.mean(x, axis=0)
    std = np.std(x, axis=0)
    print(mean, std)

print(len(tm))

stat(acc)


exit()

# accfft = np.fft.fft(acc, axis=0)
# print(accfft.shape)
# for i in range(accfft.shape[0]):
    # if i > 5 and i < accfft.shape[0]-5:
        # accfft[i,:] *= 0
# acc = np.fft.ifft(accfft, axis=0)
# plt.plot(np.abs(accfft))
# plt.show()

# np.random.shuffle(acc)
# acc -= np.mean(acc, axis=0)

newacc = acc * 0
K = 100
for i in range(-K, K+1):
    newacc += np.concatenate((acc[i:], acc[:i]), axis=0)
acc = newacc / (2*K+1)


# accfft = np.fft.fft(acc)

plt.plot(tm, acc)
# plt.plot(accfft)
plt.show()
# exit()


dt = np.diff(tm)
dt = np.concatenate(([0], dt))

vel = np.cumsum(acc * dt.reshape((dt.shape[0], 1)), axis=0)
# vel -= np.mean(vel, axis=0)
pos = np.cumsum(vel * dt.reshape((dt.shape[0], 1)), axis=0)

stat(vel)
plt.plot(tm, vel)
plt.show()

stat(pos)
plt.plot(tm, pos)
plt.show()

