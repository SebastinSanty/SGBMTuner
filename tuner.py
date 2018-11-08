from flask import Flask, render_template, request, url_for
import os
import json
import cv2
import numpy as np

# PEOPLE_FOLDER = os.path.join('images')

app = Flask(__name__)

# app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/index')
def show_index():
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'left.jpg')
    return render_template("index.html")

@app.route('/update', methods=['POST'])
def update():
    minDisparity = request.form["minDisparity"]
    numDisparities = request.form["numDisparities"]
    blockSize = request.form["blockSize"]
    disp12MaxDiff = request.form["disp12MaxDiff"]
    uniquenessRatio = request.form["uniquenessRatio"]
    speckleWindowSize = request.form["speckleWindowSize"]
    speckleRange = request.form["speckleRange"]
    preFilterCap = request.form["preFilterCap"]
    windowSize = request.form["windowSize"]

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=int(minDisparity),
        numDisparities=int(numDisparities),
        blockSize=int(blockSize),
        P1=8 * 3 * int(windowSize) ** 2,
        P2=32 * 3 * int(windowSize) ** 2,
        disp12MaxDiff=int(disp12MaxDiff),
        uniquenessRatio=int(uniquenessRatio),
        speckleWindowSize=int(speckleWindowSize),
        speckleRange=int(speckleRange),
        preFilterCap=int(preFilterCap),
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    # window_size = 3

    # left_matcher = cv2.StereoSGBM_create(
    #     minDisparity=0,
    #     numDisparities=80,             # max_disp has to be dividable by 16 f. E. HH 192, 256
    #     blockSize=5,
    #     # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    #     P1=8 * 3 * window_size ** 2,
    #     P2=32 * 3 * window_size ** 2,
    #     disp12MaxDiff=1,
    #     uniquenessRatio=15,
    #     speckleWindowSize=0,
    #     speckleRange=2,
    #     preFilterCap=63,
    #     mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    # )

    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    imgL = cv2.imread('static/left.jpg')
    imgR = cv2.imread('static/right.jpg')

    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)

    filteredImg = wls_filter.filter(displ, imgR, None, dispr)

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
    filteredImg = np.uint8(filteredImg)

    filteredImg = cv2.medianBlur(filteredImg, 9)
    # filteredImg = cv2.Canny(filteredImg, 100, 200)
    filteredImg = np.stack((filteredImg,)*3, axis=-1)
    cv2.imwrite('static/result.jpg', filteredImg)

    return json.dumps({'status': 'OK'})
