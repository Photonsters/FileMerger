#TODO:
#   form some reason on save the 
#   placement of objects is mirrored horizontally (on landscape)

import tkinter 
import tkinter.ttk as ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

from Toolbar import Toolbar
from ProgressDialog import showProgress
from PhotonFile import *
try:
    import cv2 
    cv2Available = True
    #print("Numpy library available.")
except ImportError:
    cv2Available = False
    raise Exception ("PhotonFile needs the OpenCV2 library!")
    #print ("Numpy library not found.")

       
installpath=''
root=None
scale=0.25
  
def init():
    global installpath
    if getattr(sys, 'frozen', False):# frozen
        installpath = os.path.dirname(sys.executable)
    else: # unfrozen
        installpath = os.path.dirname(os.path.realpath(__file__))
    print ("Installed at: ",installpath)

def createWindow():
    global root
    # setup window
    root = tkinter.Tk()
    root.geometry("%dx%d+0+0" % (2560/4+320+30,1440/4+61))
    root.title("Photonsters File Merger")
    root.name="root"

    iconfilepath=os.path.join(installpath+"/PhotonMerger.png")
    #print("icon",iconfilepath)
    imgicon = tkinter.PhotoImage(file=iconfilepath)
    root.tk.call('wm', 'iconphoto', root._w, imgicon) 

    return root

mouseRectColor='white'
uvColor='#8A2BE2'
def createWindowLayout():
    global root, center, body, left,right,header,footer,canvas,listbox
    global scale, fileRot,mouseRect,mouseRectColor,mouseLabel,uvColor
    defaultbg = root.cget('bg')
    debug=False  

    root.grid_columnconfigure(0,weight=1)
    root.grid_rowconfigure(0,weight=0)
    root.grid_rowconfigure(1,weight=1)
    root.grid_rowconfigure(2,weight=0)
    root.bind("<Motion>",root_movemouse)    

    header= tkinter.Frame(root,bg="yellow" if debug else defaultbg,padx=4,pady=4)
    header.name="header"
    header.grid(column=0,row=0,sticky="nesw")

    center= tkinter.Frame(root,bg="magenta2" if debug else defaultbg,padx=4,pady=4)
    center.name="center"
    center.grid(column=0,row=1,sticky="nesw")

    footer= tkinter.Frame(root,bg="yellow" if debug else defaultbg)
    footer.name="footer"
    footer.grid(column=0,row=2,sticky="nesw")

    center.grid_columnconfigure(0,weight=0)
    center.grid_columnconfigure(1,weight=1)
    center.grid_columnconfigure(2,weight=0)
    center.grid_rowconfigure(0,weight=1)

    #left = tkinter.Frame(center,width=32,bg='green' if debug else defaultbg)
    #left = tkinter.Listbox(center,width=20,bg='green' if debug else defaultbg)
    left = tkinter.Frame(center,bg='green' if debug else defaultbg)
    scrollbar = tkinter.Scrollbar(left, orient=tkinter.VERTICAL)
    listbox = tkinter.Listbox(left, yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)  
    left.name='left'
    left.grid(column=0,row=0,sticky="nsw",padx=(0,4))

    listbox.bind("<<ListboxSelect>>", listbox_select)

    middle = tkinter.Canvas(center,cursor='dot',width=int(2560*scale),height=int(1440*scale),bg=uvColor)
    middle.name='middle'
    middle.grid(column=1,row=0,sticky="nsew")
    canvas=middle
    canvas.bind("<Button-1>", canvas_clickLeft)
    canvas.bind("<Button-3>", canvas_clickRight)
    canvas.bind("<Motion>",canvas_movemouse)
    mouseRect=canvas.create_rectangle(0, 0, 0, 0, fill='',outline=mouseRectColor)
    mouseLabel=canvas.create_text(0, 0, anchor="nw", text=str(fileRot),font="Times 12 bold",fill=uvColor)

    right = tkinter.Frame(center,width=32,bg='green' if debug else defaultbg)
    right.name='right'
    right.grid(column=2,row=0,sticky="nse",padx=(4,8))

    # Toolbar
    tbEdit=Toolbar(header,orientation=tkinter.HORIZONTAL,btnSize=24)
    tbEdit.grid(column=0,row=0,sticky="wns")
    tbEdit.add_command(os.path.join(installpath,"new.png"),"New",mnNew)
    tbEdit.add_command(os.path.join(installpath,"load.png"),"Load",mnLoad)
    tbEdit.add_command(os.path.join(installpath,"save.png"),"Save",mnSaveAs)

    #Props
    global entry_BottomLayers,entry_BottomExp,entry_NormalExp,entry_Offtime,label_layerHeight
    right.columnconfigure(0, weight=0)
    right.columnconfigure(1, weight=1)

    #Bottom props
    propLabel=tkinter.Label(right,text="Bottom",font=('Helvetica', 11, 'bold'))#,bg=col)
    propLabel.grid(row=0,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    propLabel=tkinter.Label(right,text="  # Layers",font=('Helvetica', 11, ''))#,bg=col)
    propLabel.grid(row=1,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    entry_BottomLayers = tkinter.Entry(right,width=6,highlightcolor='blue')
    entry_BottomLayers.grid(row=1,column=1,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    propLabel=tkinter.Label(right,text="  Exp Time",font=('Helvetica', 11, ''))#,bg=col)
    propLabel.grid(row=2,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    entry_BottomExp = tkinter.Entry(right,width=6,highlightcolor='blue')
    entry_BottomExp.grid(row=2,column=1,padx=0,pady=0,sticky=tkinter.W+tkinter.W)

    # sep
    propLabel=tkinter.Label(right,text=" ",font=('Helvetica', 11, 'bold'))#,bg=col)
    propLabel.grid(row=3,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)

    #Normal props
    propLabel=tkinter.Label(right,text="Normal",font=('Helvetica', 11, 'bold'))#,bg=col)
    propLabel.grid(row=4,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    propLabel=tkinter.Label(right,text="  Exp Time",font=('Helvetica', 11, ''))#,bg=col)
    propLabel.grid(row=5,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    entry_NormalExp = tkinter.Entry(right,width=6,highlightcolor='blue')
    entry_NormalExp.grid(row=5,column=1,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    propLabel=tkinter.Label(right,text="  Off Time",font=('Helvetica', 11, ''))#,bg=col)
    propLabel.grid(row=6,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    entry_Offtime = tkinter.Entry(right,width=6,highlightcolor='blue')
    entry_Offtime.grid(row=6,column=1,padx=0,pady=0,sticky=tkinter.W+tkinter.W)

    # sep
    propLabel=tkinter.Label(right,text=" ",font=('Helvetica', 11, 'bold'))#,bg=col)
    propLabel.grid(row=7,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)

    #LayerHeight
    propLabel=tkinter.Label(right,text="Layer Height",font=('Helvetica', 11, 'bold'))#,bg=col)
    propLabel.grid(row=8,column=0,padx=0,pady=0,sticky=tkinter.W+tkinter.W)
    label_layerHeight=tkinter.Label(right,text="  0.5",font=('Helvetica', 11, ''))#,bg=col)
    label_layerHeight.grid(row=9,column=1,padx=0,pady=0,sticky=tkinter.W+tkinter.W)


def mnSaveAs():
    global objects
    # Check if we got a filename
    filename =  tkinter.filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("photon files","*.photon"),("all files","*.*")))
    if not filename: return  

    print ("Saving...",filename)

    # Create new photonfile
    global entry_BottomLayers,entry_BottomExp,entry_NormalExp,entry_Offtime,layerHeight,scale
    outPhotonFile=PhotonFile()
    outPhotonFile.new()
    outPhotonFile.layers.clear()
    outPhotonFile.filename=filename
    outPhotonFile.setProperty("# Bottom Layers",int(entry_BottomLayers.get()))
    outPhotonFile.setProperty("Exp. time (s)",float(entry_NormalExp.get()))
    outPhotonFile.setProperty("Exp. bottom (s)",float(entry_BottomExp.get()))
    outPhotonFile.setProperty("Off time (s)",float(entry_Offtime.get()))
    outPhotonFile.setProperty("Layer height (mm)",float(layerHeight))
    #return

    # Check max layer
    nrLayers=0
    for obj in objects:
        file=obj[0]
        photonfile=file[2]
        nrLayers=max(nrLayers,photonfile.layers.count())

    # Show messagebox to let use know we are analyzing
    app = showProgress(root,"Merging...", 0,1,True,False,False)

    # Construct each layer
    for layerNr in range(nrLayers): 
        totIm=numpy.zeros((2560,1440,1),dtype=numpy.uint8)
        for obj in objects:
            file,xdest,ydest,wdest,hdest,rot=obj
            #print ("obj: ",xdest,ydest,wdest,hdest,rot,file)
            (xdest,ydest)=(ydest,xdest)
            xdest=int(xdest/scale)
            ydest=int(ydest/scale)
            wdest,hdest=file[4]
            if rot==90: wdest,hdest=hdest,wdest
            #if layerNr<10:
            #    print ("dest2",xdest,ydest,wdest,hdest)
            #file entries are tuples of:filename,photonfile classobject,position,size
            idx,filename,photonfile,(xsrc,ysrc),(wsrc,hsrc)=file
            # check if this photonfile has enough layers
            #print (photonfile.layers.count(),">",layerNr)
            if layerNr<photonfile.layers.count():
                # Get full layer
                locIm=photonfile.layers.get(layerNr,'i')
                # Get active region in layer
                locIm=locIm[ysrc:ysrc+hsrc,xsrc:xsrc+wsrc]
                # Rotate if requested
                #print ("shape1:",locIm.shape)
                if rot==90: locIm=numpy.rot90(locIm)
                #print ("shape2:",locIm.shape)
                # Put in destination
                #print ("dest:  [",ydest,":",ydest+hdest,",",xdest,":",xdest+wdest,"]") 
                totIm[ydest:ydest+hdest,xdest:xdest+wdest]=locIm
                if layerNr==10:
                    print ("write")
                    cv2.imwrite("test/out1.png",locIm)
                    cv2.imwrite("test/out2.png",totIm)

        # For some res                    
        outPhotonFile.layers.append(totIm)
        #if layerNr>3: return

        app.setProgressPerc(int(100*layerNr/nrLayers))

    app.hide()


    outPhotonFile.save()

def mnLoad():
    global layerHeight
    filename =  tkinter.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("photon files","*.photon"),("all files","*.*")))
    if not filename: return
    photonfile=readPhotonFile(filename)

layerHeight=-1
def readPhotonFile(filename):
    global files
    global layerHeight

    photonfile=PhotonFile()    
    photonfile.load(filename)

    # Check if file not already present
    for file in files:
        if file[1]==filename:
            root.option_add('*Dialog.msg.font', 'Helvetica 10')    
            messagebox.showerror('File already loaded','You already loaded this file.')
            return

    # If first file we copy properties
    if len(files)==0: 
        layerHeight=photonfile.getProperty("Layer height (mm)")

        entry_BottomLayers.delete(0,tkinter.END)
        entry_NormalExp.delete(0,tkinter.END)
        entry_BottomExp.delete(0,tkinter.END)
        entry_Offtime.delete(0,tkinter.END)
        entry_BottomLayers.insert(0,photonfile.getProperty("# Bottom Layers"))
        entry_NormalExp.insert(0,photonfile.getProperty("Exp. time (s)"))
        entry_BottomExp.insert(0,photonfile.getProperty("Exp. bottom (s)"))
        entry_Offtime.insert(0,photonfile.getProperty("Off time (s)"))
    
    # Check if layerheight is same as other layerheights
    if photonfile.getProperty("Layer height (mm)")!=layerHeight:
        root.option_add('*Dialog.msg.font', 'Helvetica 10')    
        messagebox.showerror('Different Layer Height','All photonfiles should have samen layerheight.')
        return

    # set layerheight
    label_layerHeight['text']=str(layerHeight)

    # Show messagebox to let use know we are analyzing
    app = showProgress(root,"Analyzing...", 0,1,True,False,False)

    xmin,ymin,xmax,ymax=9999,9999,0,0
    for layerNr in range(photonfile.layers.count()):
        im=photonfile.layers.get(layerNr,'n') # 2560 rows, 1440 cols; element is called im[y,x]
        res=cv2.findContours(im.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # In the current OpenCV's master branch the return statements have changed, see http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html?highlight=findcontours.
        if len(res)==3: _,contours,hierarchy=res
        if len(res)==2: contours,hierarchy=res
        #contours, hierarchy = cv2.findContours(im.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        idx = 0 
        for cnt in contours:
            idx += 1
            x,y,w,h = cv2.boundingRect(cnt)
            xmin=min(x,xmin)
            ymin=min(y,ymin)
            xmax=max(x+w,xmax)
            ymax=max(y+h,ymax)

        app.setProgressPerc(int(100*layerNr/photonfile.layers.count()))

    app.hide()

    #put some margin around regions
    margin=10
    def clamp(n, smallest, largest): return max(smallest, min(n, largest))
    xmin=clamp(xmin-margin,0,1439)
    ymin=clamp(ymin-margin,0,2559)
    xmax=clamp(xmax+margin,0,1439)
    ymax=clamp(ymax+margin,0,2559)
    
    #files entries are tuples of:filename,photonfile classobject,position,size
    files.append([len(files),filename,photonfile,(xmin,ymin),(xmax-xmin,ymax-ymin)])

    print ("Read:",filename,photonfile.layers.count(),(xmin,ymin),(xmax-xmin,ymax-ymin))
    print ("Read:",files[len(files)-1])

    basename=os.path.basename(filename)
    barename=os.path.splitext(basename)[0]
    item=str(len(files))+" "+barename
    listbox.insert(tkinter.END, item)

    return photonfile

def mnNew():
    global objects,files,canvas,layerHeight,fileIdx,fileRot,listbox,label_layerHeight,mouseRect,mouseRectColor
    objects=[]
    files=[]
    canvas.delete("all")
    layerHeight=-1
    fileIdx=-1
    listbox.delete(0,tkinter.END)
    label_layerHeight['text']=''
    mouseRect=canvas.create_rectangle(0, 0, 0, 0, fill='',outline=mouseRectColor)
    mouseLabel=canvas.create_text(0, 0, anchor="nw", text=str(fileRot),font="Times 12 bold",fill=uvColor)


fileIdx=-1
fileRot=0
def listbox_select(event):
    global listbox,fileIdx
    fileIdx = event.widget.curselection()[0]
    print (fileIdx)    

def root_movemouse(event):
    # canvas_mousemove does not get all mouse events when moving out of left or top border
    # this method serves as to detect them and hide the cursor rect in canvas
    global uvColor,canvas
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)    
    if widget!=canvas:
        canvas.coords(mouseRect, (0,0,0,0))
        canvas.coords(mouseLabel,(0,0))
        canvas.itemconfig(mouseLabel,fill=uvColor)
    
def canvas_movemouse(event):
    global canvas,mouseRect,mouseLabel,fileIdx,fileRot,scale,uvColor
    coords=canvas.coords(mouseRect)
    coords=[0,0,0,0]
    fillColor=uvColor
    #Only display if we have file selected
    if fileIdx>-1: 
        x,y=event.x,event.y   
        #print ("x,y:",x,y)
        file=files[fileIdx]
        h,w=file[4]  # we show GUI landscape but slices are stored in portrait
        h=int(h*scale)
        w=int(w*scale)
        if fileRot!=0:w,h=h,w
        # Only display if in boundaries of layer (0:2560, 0:1440)
        if x>0 and y>0 and (x+w)<2560*scale and (y+h)<1440*scale:
            # Only display if not overlapping with other rect
            rect=(x,y,x+w,y+h)
            if not inObject(rect):
                coords=x,y,x+w,y+h
                fillColor='white'

    canvas.coords(mouseRect, coords)
    canvas.coords(mouseLabel,(coords[0]+2,coords[1]))
    canvas.itemconfig(mouseLabel,fill=fillColor)
    canvas.tag_raise(mouseRect)

def canvas_clickRight(event):
    global fileRot
    fileRot=90 if fileRot==0 else 0
    canvas.itemconfig(mouseLabel,text=str(fileRot))
    # recheck if this rect fits on empty space
    canvas_movemouse(event)

def canvas_clickLeft(event):
    global canvas,fileIdx,fileRot,files,objects,mouseRect,mouseLabel
    x,y=event.x, event.y
    objIdx=findObject(x,y)
    # If we clicked existing rectangle, we empty canvas, remove object/rect and redraw rest
    if objIdx!=-1: 
        del objects[objIdx]
        canvas.delete("all")
        for obj in objects:            
            (file,x,y,w,h,rot)=obj
            canvas.create_rectangle(x, y, x+w, y+h, fill='red')
            canvas.create_text(x+2, y, anchor="nw", text=str(file[0]+1),font="Times 12 italic bold")
        mouseRect=canvas.create_rectangle(0, 0, 0, 0, fill='',outline=mouseRectColor)
        mouseLabel=canvas.create_text(0, 0, anchor="nw", text=str(fileRot),font="Times 12 bold",fill=uvColor)
        print ("Removed object")
        print ("Nr Objects:",len(objects))
        return

    # else we clicked on empty space
    # Check if we have file selected in left bar
    if fileIdx==-1: return

    file=files[fileIdx]
    h,w=file[4]  # we show GUI landscape but slices are stored in portrait
    h=int(h*scale)
    w=int(w*scale)
    if fileRot!=0: w,h=h,w

    # Only if in boundaries of layer (0:2560, 0:1440)
    if x>0 and y>0 and (x+w)<2560*scale and (y+h)<1440*scale:
        # Only display if not overlapping with other rect
        if not inObject((x,y,x+w,y+h)):
            canvas.create_rectangle(x, y, x+w, y+h, fill='red')
            canvas.create_text(x+2, y, anchor="nw", text=str(file[0]+1),font="Times 12 bold")
            objects.append([file,x,y,w,h,fileRot])

    print ("Added object:", file)
    print ("Nr Objects:",len(objects))

def inObject(rect):
    #rect should be tuple of (x1,y1,x2,y2)
    xr1,yr1,xr2,yr2=rect

    for idx,obj in enumerate(objects):
        xo1,yo1,wo,ho,rot=obj[1:]
        xo2=xo1+wo
        yo2=yo1+ho

        # no intersection if rect left,right, above or below of obj
        noOverlap = xr2<xo1 or xr1>xo2 or yr2<yo1 or yr1>yo2
        if not noOverlap: return True

    return False

def findObject(mouseX,mouseY):
    for idx,obj in enumerate(objects):
        file,x,y,w,h,rot=obj
        if mouseX>x and mouseY>y and mouseX<(x+w) and mouseY<(y+h):
            print (idx)
            return idx
    return -1

files=[]
objects=[]

init()
createWindow()
createWindowLayout()

#readPhotonFile("test/cylinder and 20x20x20 sideways.photon")
#readPhotonFile("test/20x20x20.photon")
#readPhotonFile("test/bunny_small.photon")
#readPhotonFile("test/cylinder.photon")
#readPhotonFile("test/cylinder and 20x20x20.photon")

root.update()
root.minsize(root.winfo_width(), root.winfo_height())    
root.maxsize(root.winfo_width(), root.winfo_height())  
root.mainloop()