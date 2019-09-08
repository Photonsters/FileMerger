# Photonsters FileMerger

The FileMerger is a utility to combine/merge several photon files into a new one.

This saves a lot of time when you have a lot of photon files of singular miniature models, which you occasionally reprint in different amounts. 

- You can off course use ChiTuBox to add all stls, add supports (propbably manual placement is needed, see [3DPrintingPro](https://www.youtube.com/channel/UCbv2mDrRqXovPdahRyoCFhA) for tips) and then run [Validator](https://github.com/Photonsters/PhotonFileValidator) to fix all islands to small for supports.
- But if you already have supported and validated photon files per model, with this tool you can combine these photonfiles as you need.

FileMerger is programmed in Python 3.6 and uses the additional libraries Cython (fast compression / mesh calculations), OpenCV (image drawing routines) and numpy (handling large image data).

## Disclaimer
FileMerger is alpha. There probably are bugs, the output files have not yet been tested on a real photon! Use at your own risk!

 ---
  
## Installation
You can run FileMerger in Windows, OSX and Linux. There is no binary release so you have to install Python3

0) Download the source code in zip or tar.gz.
1) Install Python **3** from https://www.python.org/downloads/  
__or__ install Anaconda 3.6 https://www.anaconda.com/download/ 
2) Check the python version is above 3 by typing in the command line 'python --version'
3) Install the numpy and opencv libraries
   * type 'python -m pip install -U numpy --user'
   * type 'python -m pip install -U cv2 --user'
4) You have two options to run PhotonFileMerger:
   * from your file explorer find and run PhotonFileMerger.py 
   * from a dos prompt/linux terminal, navigate to the directory where you extracted the zip file and type 'phyton PhotonFileMerger.py' for windows or 'phyton3 PhotonFileMerger.py' for linux.

**Attention: PhotonFileMerger will not work with Python 2!** 

---
  
    
## Manual

If you start FileMerger you are presented the following screen:
![image](https://user-images.githubusercontent.com/11459480/64485760-bfcc3e80-d224-11e9-9b61-c5aa7af523aa.png)

### Window layout
__Toolbar__: The buttons at the top allow you start fresh, load files to merge and save the merged file.  
__File area__: The white box on the left lists all photon files you have loaded.  
__Layout area__: The blue box in the middle shows the layout of the merged photon file  
__Properties area__: The grey area on the right shows the print properties of the merged photon file. Per default the properties of the first loaded file are used.  

__Remarks__:
You can only merge files which have the same layerheight.
The layout area will only allow placement of a source photon file (and show a rectangle) if there is room at the cursor.

### Load files: ![image](https://user-images.githubusercontent.com/11459480/64485766-c65ab600-d224-11e9-8094-78ddf93c1717.png)

![image](https://user-images.githubusercontent.com/11459480/64485761-c064d500-d224-11e9-96c5-f49090eabe2d.png)

Use the load button to load all photon files you want to combine. On each load FileMerger will analyse the photonfile you selected and extract the 3D-model (voxel-area) in it.

If you want to clear all models in the __File area__, use the new button: ![image](https://user-images.githubusercontent.com/11459480/64485767-c6f34c80-d224-11e9-8a06-6b459eda9672.png)
  
  
### Place models
![image](https://user-images.githubusercontent.com/11459480/64485763-c064d500-d224-11e9-96f0-a4b91de4bfdc.png)
__Add:__
- Select a model in the __File area__ and move your cursor to the __Layout area__. If the layout area detects there is room at your cursor position, it displays a white rectangle.  
- Use the right mouse button to rotate the model 90 degrees.  
- Use the left mouse button to drop the model. (You can do this more than once.) A red rectangle appear with a number in the top left indicating the model from the __File area__.     

__Remove:__
- Move your mouse cursor on top a placed model/red rectangle and use your left mouse button to remove.
  
   
### Merge models (save): ![image](https://user-images.githubusercontent.com/11459480/64485768-c6f34c80-d224-11e9-9d92-4b21e91d8b41.png)

![image](https://user-images.githubusercontent.com/11459480/64485764-c064d500-d224-11e9-8dcb-533cb69212fa.png)
Specify a name and FileMerger will construct a new photon file.





 
