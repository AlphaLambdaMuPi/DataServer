import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('data/pic1.jpg')
img2 = cv2.imread('data/pic2.jpg')

img1 = cv2.resize(img1, (480, 640), interpolation=cv2.INTER_CUBIC)
img2 = cv2.resize(img2, (480, 640), interpolation=cv2.INTER_CUBIC)

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
p1 = cv2.goodFeaturesToTrack(gray1, 200, 0.3, 7)
# fast = cv2.FastFeatureDetector()
# p0 = fast.detect(img1, None)

# cv2.drawKeypoints(img1, keypoints=p0, outImage=None, color=(255, 0, 0))

lk_params = dict( winSize  = (15,15), maxLevel = 20,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


p2, st, err = cv2.calcOpticalFlowPyrLK(gray1, gray2, p1, None, **lk_params)

flow = cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

# stereo = cv2.StereoSGBM_create(0, numDisparities=16, blockSize=15)

# plt.figure(1)
# disparity = stereo.compute(gray1, gray2)
# plt.imshow(disparity)

# plt.figure(1)
# x, y = np.meshgrid(np.arange(0, 480, 40), np.arange(0, 640, 40))
# plt.imshow(img1[:,:,::-1], cmap = 'gray', interpolation = 'bicubic')
# plt.quiver(x, y, flow[y,x,0], flow[y,x,1])

plt.figure(1)
plt.imshow(img1[:,:,::-1], cmap = 'gray', interpolation = 'bicubic')
plt.scatter(p1[:, 0, 0], p1[:, 0, 1], s=err*2)

plt.figure(2)
plt.imshow(img2[:,:,::-1], cmap = 'gray', interpolation = 'bicubic')
plt.scatter(p2[:, 0, 0], p2[:, 0, 1], s=err*2)
plt.show()

