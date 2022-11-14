# Nighttime image enhancement using a new illumination boost algorithm
Repository which replicates the results obtained by Al-Ameen, Zohair in his paper entitled  _[Nighttime image enhancement using a new illumination boost algorithm](https://ieeexplore.ieee.org/document/8741330)_, published at [IET Image Processing Journal](https://digital-library.theiet.org/content/journals/iet-ipr).

The code was implemented using MATLAB, following the steps presented in the paper. And translated to Python using OpenCV, Numpy and SciPy.

## Usage (MATLAB)
The [`illumination_boost.m`](./illumination_boost.m) file contains the main (and only) function for the algorithm. It accepts an RGB image, and a Lambda parameter used in equations `4` and `6` in the paper, which, according to the paper, acquire best results with values between 2 and 7. It returns an RGB image with `double` type.

A test file named [`test_illumination_boost.m`](./test_illumination_boost.m) is made available, to test the function with the images available in the [`input_images`](./input_images/) folder, varying the lambda parameter from 2 to 6.

There is also the file [`plot_with_histogram.m`](./plot_with_histogram.m) which generates histograms for the base image and the enhanced one, given an image and a lambda parameter.

## Usage (Python)
The [`illumination_boost.py`](./illumination_boost.py) file contains the main (and only) function for the algorithm. It accepts an RGB image, and a Lambda parameter used in equations `4` and `6` in the paper, which, according to the paper, acquire best results with values between 2 and 7. It returns an RGB image with `uint8` dtype.

### Testing on image dataset
To test on the image dataset, you can use the following command:
```bash
python test_illumination_boost.py
```
The program will iterate on all the files inside the **input_images** folder, and generate new images with the following name pattern ``filename_comparison.jpg`` inside the **output_images** folder.

### Testing on webcam
To test directly on your webcam, you can use the following command:
```bash
python test_illumination_boost_on_camera.py
```
The program will try to open the first/default webcam on your computer and show side-by-side original and boosted image.

## Results
Several results are available in the [`output_images`](./output_images/) folder, and some of them are displayed below:
![cat-example](./output_images/cat.jpg)
![airplane-example](./output_images/airplane.jpg)
![building-example](./output_images/building.jpg)
![girl-example](./output_images/girl.jpg)
![clock-example](./output_images/clock.jpg)
![maze-example](./output_images/maze.jpg)

## Disclaimer
This repository is not endorssed and/or affiliated in any way to Al-Ameen, Zohair. The paper was replicated for purely didactic purposes.