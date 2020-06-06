# SELF-DRIVING BOT FOR GTA
The goal of this project is to make an intelligent bot that can drive a car or motorcycle in Grand Theft Auto V. 

# MOTIVATION
This is a project for the Machine Learning course (COEN 140) at Santa Clara University. Our group wanted to work on something that was challenging and interesting to all involved. Through this project, we got to explore interacting with the world of GTA while building on our knowledge of Python, OpenCV, and deep learning techniques. 

The best possible way to see how well an AI drives a car -- for us as students -- is through an open-world game like GTA which does not have potential to cause harm.

# HOW TO USE IT
To see the results of lane detection, navigate to the /lane-detection subfolder which contains multiple test images along with the algorithm to find lanes. The file "cv.py" is provided which on execution generates the results and pushes them to the active window as keypresses, while displaying image results in a seperate window.

To test out the neural network, first drive around on GTA V to generate some training data (or download publically available training data!); "generate.py" is provided for this purpose (which expects that you run the game at 800x600, in the top left corner of the screen). It is also assumed that you are on a Windows machine (pywin32 is a required library). After generating training data (which should be placed in the /training subfolder within the /neural_network subfolder),
use "train.py" to create a model using TFLearn's implementation of Alexnet.

Once the model has been created, move it to the /models subfolder. Then run "main.py" and the neural network should begin!

# TASK LIST
- [X] Grab screen images of the game 
- [X] Interact directly with the game via python
- [X] Detect street lanes for navigation
- [X] Apply deep learning algorithms for self driving

# AUTHORS
Omar Garcia and Jay Ladhad
