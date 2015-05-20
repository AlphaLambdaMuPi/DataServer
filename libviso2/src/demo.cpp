/*
   Copyright 2012. All rights reserved.
   Institute of Measurement and Control Systems
   Karlsruhe Institute of Technology, Germany

   This file is part of libviso2.
Authors: Andreas Geiger

libviso2 is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or any later version.

libviso2 is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
libviso2; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA
*/

/*
   Documented C++ sample code of stereo visual odometry (modify to your needs)
   To run this demonstration, download the Karlsruhe dataset sequence
   '2010_03_09_drive_0019' from: www.cvlibs.net!
Usage: ./viso2 path/to/sequence/2010_03_09_drive_0019
*/

#include <iostream>
#include <string>
#include <vector>
#include <stdint.h>

#include <viso_stereo.h>
#include <viso_mono.h>
#include <png++/png.hpp>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

const int WID = 240*2;
const int HEI = 320*2;
// const int WID = 1344;
// const int HEI = 391;

int main(int argc, char** argv)
{

    // set most important visual odometry parameters
    // for a full parameter list, look at: viso_stereo.h
    VisualOdometryMono::parameters param;

    // calibration parameters for sequence 2010_03_09_drive_0019
    param.calib.f  = WID; // focal length in pixels
    param.calib.cu = WID / 2; // principal point (u-coordinate) in pixels
    param.calib.cv = HEI / 2; // principal point (v-coordinate) in pixels
    // param.calib.f  = 645.24; // focal length in pixels
    // param.calib.cu = 635.96; // principal point (u-coordinate) in pixels
    // param.calib.cv = 194.13; // principal point (v-coordinate) in pixels
    // param.inlier_threshold = 3E-5;
    param.motion_threshold = 200;
    param.bucket.bucket_width = WID/16;
    param.bucket.bucket_height = HEI/16;
    param.bucket.max_features = 3;

    // init visual odometry
    // VisualOdometryStereo viso(param);
    VisualOdometryMono viso(param);

    // current pose (this matrix transforms a point from the current
    // frame's camera coordinates to the first frame's camera coordinates)
    Matrix pose = Matrix::eye(4);

    int sig;
    int cnt = -1;
    while (~scanf("%d", &sig)) {
        cnt++;

        // input file names
        // string left_img_file_name  = "img/I1c.png";
        // string x[6] = {"img/a1.jpg", "img/a2.jpg", "img/a3.jpg", "img/a4.jpg", "img/a5.jpg", "img/a6.jpg"};
        // string x[4] = {"img/b001.jpg", "img/b002.jpg", "img/b003.jpg", "img/b004.jpg"};
        // string x[6] = {"img/I1c.png", "img/I1p.png", "img/I2c.png", "img/I2p.png"};

        // catch image read/write errors here
        try {

            // load left and right input image
            // string left_img_file_name  = x[cnt%4];
            char trf[1000];
            sprintf(trf, "img/b%03d.jpg", (cnt%500)+1);
            string left_img_file_name = trf;
            cout<<left_img_file_name<<endl;
            // png::image< png::gray_pixel > left_img(left_img_file_name);
            Mat left_img;
            left_img = imread(left_img_file_name, CV_LOAD_IMAGE_GRAYSCALE);
            resize(left_img, left_img, Size(WID, HEI));
            // CImg<unsigned char> left_img(left_img_file_name.c_str());

            // image dimensions
            // int32_t width  = left_img.get_width();
            // int32_t height = left_img.get_height();
            int32_t width  = left_img.cols;
            int32_t height = left_img.rows;
            cout<<width<<" X "<<height<<endl;

            // convert input images to uint8_t buffer
            uint8_t* left_img_data  = (uint8_t*)malloc(width * height * sizeof(uint8_t));
            int k = 0;
            for (int v = 0; v < height; v++) {
                for (int u = 0; u < width; u++) {
                    // left_img_data[k]  = left_img.get_pixel(u, v);
                    left_img_data[k] = left_img.at<uint8_t>(v, u);
                    k++;
                }
            }

            // compute visual odometry
            int32_t dims[] = {width, height, width};
            if (viso.process(left_img_data, dims)) {

                // on success, update current pose
                Matrix mot = Matrix::inv(viso.getMotion());
                pose = pose * mot; 

                // output some statistics
                double num_matches = viso.getNumberOfMatches();
                double num_inliers = viso.getNumberOfInliers();
                cout << ", Matches: " << num_matches;
                cout << ", Inliers: " << 100.0 * num_inliers / num_matches << " %" << ", Current pose: " << endl;
                cout << pose << endl << endl;
                // cout << mot << endl << endl;
                // cout << pose.val[0][3] << " " << pose.val[1][3] << " " << pose.val[2][3] << endl;
                vector<int> inliers = viso.getInlierIndices();
                vector<Matcher::p_match> matches = viso.getMatches();
                for(int i=0; i<num_inliers; i++)
                {
                    Matcher::p_match pmat = matches[inliers[i]];
                    int u = pmat.u1c, v = pmat.v1c;
                    left_img.at<uint8_t>(v, u) = 255;
                    left_img.at<uint8_t>(v+1, u) = 0;
                    left_img.at<uint8_t>(v-1, u) = 0;
                    left_img.at<uint8_t>(v, u+1) = 0;
                    left_img.at<uint8_t>(v, u-1) = 0;
                }
                imwrite("AAA.jpg", left_img);

            }
            else {
                cout << " ... failed!" << endl;
            }

            // release uint8_t buffers
            free(left_img_data);

            // catch image read errors here
        }
        catch (...) {
            cerr << "ERROR: Couldn't read input files!" << endl;
            return 1;
        }
    }

    // exit
    return 0;
}

