import numpy as np
import scipy
from scipy import stats
import json
import matplotlib.pyplot as plt

f = list(open('data/Nexus-5-2.txt'))
f = [json.loads(x.strip('\n')) for x in f]

acc = []
tm = []
for d in f:
    if d['type'] != 'accel':
        continue
    tm.append(d['time'])
    acc.append(json.loads(d['data']))

acc = np.array(acc)
tm = np.array(tm) / 1E9
tm -= tm[0]

def stat(x):
    mean = np.mean(x, axis=0)
    std = np.std(x, axis=0)
    print(mean, std)

print(len(tm))

stat(acc)

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

