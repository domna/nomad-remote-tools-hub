from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import apt_importers_1_3 as apt
import math
from matplotlib import gridspec

class APT_analyzer():                                                          # define class object 
    def __init__(self,tk):                                                     # initialize when starting tkinter
        self.data_color=('red','green','blue','black')                         # colors of cylinder to be seletected
        self.frame=Frame(tk)                                                   # setting up frame
        self.frame.pack(expand=True,fill=BOTH)                                 # placing frame
        self.canvas_all=Canvas(self.frame,width=1400,height=800,scrollregion=(0,0,1550,850))     #setting up canvas onto frame
        
        ################# scroll bars vertical and horizontal  ################
        self.hbar=Scrollbar(self.frame,orient=HORIZONTAL)                      # setting up horizontal scrollbar
        self.hbar.pack(side=TOP,fill=X)                                        # placing horizontal scrollbar on the top side
        self.hbar.config(command=self.canvas_all.xview)                        # configurating horizontal scrollbar
        self.vbar=Scrollbar(self.frame,orient=VERTICAL)                        # setting up vertical scrollbar
        self.vbar.pack(side=LEFT,fill=Y)                                       # placing vertical scrollbar on the left side
        self.vbar.config(command=self.canvas_all.yview)                        # configurating vertical scrollbar
        self.canvas_all.config(yscrollcommand=self.vbar.set,xscrollcommand=self.hbar.set)       #configurating canvas
        
        
        ############## setting up buttons for file selection ##################
        self.label_init_files=Label(self.canvas_all,text='------------- initiate files --------------')    # title of segment
        self.canvas_all.create_window(200,35,window=self.label_init_files)
        self.b_pos_file = Button(self.canvas_all, text=".pos /.epos file", command=self.search_pos)        # button for pos file initiation
        self.canvas_all.create_window(120,70,window=self.b_pos_file)
        self.b_rrng_file = Button(self.canvas_all, text=".rrng file", command=self.search_rrng)             # button for rrng file initiation
        self.canvas_all.create_window(280,70,window=self.b_rrng_file)
        self.b_calc_tip = Button(self.canvas_all, text="calculate tip", command=self.calculate_tip,bg='blue',fg='white',font=('helvetica',14,'bold')) # button for tip calculation
        self.canvas_all.create_window(200,140,window=self.b_calc_tip)
        
        
        ############## setting up buttons, Scales, comboboxes, etc. for plot options ###################
        self.label_plot_tip=Label(self.canvas_all,text='------------- plot options ---------------')    # title of segment
        self.canvas_all.create_window(200,180,window=self.label_plot_tip)
        self.b_plot = Button(self.canvas_all, text="plot tip", command=self.plot_tip,bg='blue',fg='white',font=('helvetica',14,'bold')) # button for plotting the tip
        self.canvas_all.create_window(275,730,window=self.b_plot)
        self.var_axis=IntVar()
        self.check_axis = Checkbutton(self.canvas_all,text="Hide Axis", onvalue=1, offvalue=0,variable=self.var_axis,font=('helvetica', 10,'bold'))
        self.canvas_all.create_window(100,220,window=self.check_axis)
        self.label_resolution=Label(self.canvas_all,text='Select resolution')                     # label for resolution
        self.canvas_all.create_window(100,270,window=self.label_resolution)
        self.label_select_atom=Label(self.canvas_all,text='Select atom type')
        self.canvas_all.create_window(280,210,window=self.label_select_atom)  
        self.slider_res_cv=DoubleVar()
        self.label_slider_res=Label(self.canvas_all,text='low                   high')           # title of segment
        self.canvas_all.create_window(100,290,window=self.label_slider_res)
        self.slider_res = Scale(self.canvas_all,from_=1,to=10,orient='horizontal',variable=self.slider_res_cv,showvalue=0)
        self.canvas_all.create_window(100,310,window=self.slider_res)
        self.slider_res.set(5)
        self.label_select_atom_size=Label(self.canvas_all,text='Select atom size')
        self.canvas_all.create_window(280,270,window=self.label_select_atom_size)
        self.slider_size_cv=DoubleVar()
        self.slider_size = Scale(self.canvas_all,from_=1,to=1000,orient='horizontal',variable=self.slider_size_cv)
        self.canvas_all.create_window(280,300,window=self.slider_size)
        self.slider_size.set(100)
        self.i_plot=IntVar()
        self.plot_inv=Checkbutton(self.canvas_all, text='Inverse tip', onvalue=1, offvalue=0, variable=self.i_plot, font=('helvetica', 10,'bold'))
        self.canvas_all.create_window(300,690,window=self.plot_inv)
    
        ###########  setting up buttons, Scales, comboboxes etc. for cylinder selection and concentration calculations  ###################
        self.label_conc=Label(self.canvas_all,text='------------ concentration calculation option  ------------')#.place(x=20,y=400)    # title of segment
        self.canvas_all.create_window(200,350,window=self.label_conc)
        self.var_cyl=IntVar()
        self.check_cylinder = Checkbutton(self.canvas_all,text="show cylinder for concentration calculation", onvalue=1, offvalue=0,variable=self.var_cyl,font=('helvetica', 10,'bold'))#.place(x=20,y=220)
        self.canvas_all.create_window(200,390,window=self.check_cylinder)
        
        self.b_calc_conc = Button(self.canvas_all, text="concentration", command=self.calc_con,bg='green',fg='white',font=('helvetica',12,'bold'))   # button for calculating the concentration of cylinder
        self.canvas_all.create_window(100,780,window=self.b_calc_conc)
        self.b_calc_excess = Button(self.canvas_all, text="excess", command=self.calc_excess,bg='green',fg='white',font=('helvetica',12,'bold'))    # button for calculating the concentration of cylinder
        self.canvas_all.create_window(230,780,window=self.b_calc_excess)
        self.b_plot_cyl = Button(self.canvas_all, text="cylinder", command=self.calc_zoom,bg='green',fg='white',font=('helvetica',12,'bold'))  # button for calculating the concentration of cylinder
        self.canvas_all.create_window(340,780,window=self.b_plot_cyl)
        self.b_clear = Button(self.canvas_all, text="clear", command=self.clear,bg='red',fg='white',font=('helvetica',14,'bold'))    # button for calculating the concentration of cylinder
        self.canvas_all.create_window(90,730,window=self.b_clear)
        
        self.label_cly_pos=Label(self.canvas_all,text='cylinder center position')
        self.canvas_all.create_window(200,420,window=self.label_cly_pos)
        self.label_cly_x=Label(self.canvas_all,text='x')
        self.canvas_all.create_window(100,440,window=self.label_cly_x)
        self.cly_x=StringVar(value='0')
        self.entry_cly_x=Entry(self.canvas_all,textvariable=self.cly_x,width=10)
        self.canvas_all.create_window(100,470,window=self.entry_cly_x)
        
        self.label_cly_y=Label(self.canvas_all,text='y') 
        self.canvas_all.create_window(200,440,window=self.label_cly_y)
        self.cly_y=StringVar(value='0')
        self.entry_cly_y=Entry(self.canvas_all,textvariable=self.cly_y,width=10)
        self.canvas_all.create_window(200,470,window=self.entry_cly_y)
        
        self.label_cly_z=Label(self.canvas_all,text='z')
        self.canvas_all.create_window(300,440,window=self.label_cly_z)
        self.cly_z=StringVar(value='0')
        self.entry_cly_z=Entry(self.canvas_all,textvariable=self.cly_z,width=10)
        self.canvas_all.create_window(300,470,window=self.entry_cly_z)
        
        self.label_cly_radius=Label(self.canvas_all,text='radius of cylinder')  
        self.canvas_all.create_window(100,500,window=self.label_cly_radius)
        self.radius=StringVar(value='10')
        self.entry_cly_radius=Entry(self.canvas_all,textvariable=self.radius) 
        self.canvas_all.create_window(100,525,window=self.entry_cly_radius)               
        
        self.label_cly_height=Label(self.canvas_all,text='height of cylinder') 
        self.canvas_all.create_window(300,500,window=self.label_cly_height)
        self.height=StringVar(value='30')
        self.entry_cly_height=Entry(self.canvas_all,textvariable=self.height)
        self.canvas_all.create_window(300,525,window=self.entry_cly_height) 
        
        self.label_cly_beta=Label(self.canvas_all,text='tilt along x-axis')
        self.canvas_all.create_window(100,555,window=self.label_cly_beta)
        self.beta=StringVar(value='0')
        self.entry_cly_beta=Entry(self.canvas_all,textvariable=self.beta)
        self.canvas_all.create_window(100,580,window=self.entry_cly_beta)
        
        self.label_cly_alpha=Label(self.canvas_all,text='tilt along y-axis')
        self.canvas_all.create_window(300,555,window=self.label_cly_alpha)
        self.alpha=StringVar(value='0')
        self.entry_cly_alpha=Entry(self.canvas_all,textvariable=self.alpha)
        self.canvas_all.create_window(300,580,window=self.entry_cly_alpha) 
        
        self.label_color_cyl=Label(self.canvas_all,text='colour of cylinder')   # label for cylinder color
        self.canvas_all.create_window(100,620,window=self.label_color_cyl)
        self.cb_color = Combobox(self.canvas_all, values=self.data_color)
        self.canvas_all.create_window(100,645,window=self.cb_color)
        self.cb_color.current(0)     
        
        self.label_inter=Label(self.canvas_all,text='Select interval')      # label for resolution
        self.canvas_all.create_window(300,610,window=self.label_inter)
        self.slider_inter_cv=DoubleVar()
        self.label_slider_inter=Label(self.canvas_all,text='low                   high')    # title of segment
        self.canvas_all.create_window(300,630,window=self.label_slider_inter)
        self.slider_inter = Scale(self.canvas_all,from_=1,to=10,orient='horizontal',variable=self.slider_inter_cv,showvalue=0)#Combobox(self.canvas_all, values=self.data_res)                                                            # combobox for resolution
        self.canvas_all.create_window(300,655,window=self.slider_inter)
        self.slider_inter.set(5)
        
        self.var_plot=IntVar()
        self.check_axis = Checkbutton(self.canvas_all,text="plot single", onvalue=0, offvalue=1,variable=self.var_plot,font=('helvetica', 10,'bold'))#.place(x=20,y=220)
        self.canvas_all.create_window(100,690,window=self.check_axis)
        self.check_axis = Checkbutton(self.canvas_all,text="plot all", onvalue=1, offvalue=0,variable=self.var_plot,font=('helvetica', 10,'bold'))#.place(x=20,y=220)
        self.canvas_all.create_window(200,690,window=self.check_axis)
        
        ###################### setup figures  #################################                        
        self.fig=Figure(figsize=(15,11))                                       # defining figure size
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.canvas_all)         # setting up canvas for figure
        self.toolbar=NavigationToolbar2Tk(self.canvas, self.canvas_all)        # setting up toolbar for figure
        self.canvas_all.create_window(400,10,window=self.canvas.get_tk_widget(),anchor=N+W,tags='canvas') #placing figure canvas on general canvas
        self.canvas_all.pack(expand=True,fill=BOTH)                            # placing general canvas at the end
        self.E=2                                                               # setting up variable to check if .pos/.epos file is selected
        self.R=2                                                               # setting up variable to check if .rrng file is selected       

    def search_pos(self):                                                      # function for searching for pos/epos file
        self.filename=filedialog.askopenfilename()                             # getting file from search
        S='.POS' in self.filename                                              # checking if .POS is in the filename
        ES='.EPOS' in self.filename                                            # checking if .EPOS is in the filename
        s='.pos' in self.filename                                              # checking if .pos is in the filename
        es='.epos' in self.filename                                            # checking if .epos is in the filename
        if S or s is True:                                                     # if .POS or .pos was selected
            self.label_pos_selected=Label(text='pos file selected')            # create label for pos
            self.canvas_all.create_window(120,95,window=self.label_pos_selected) #placing label on canvas
            self.E=0                                                           # set variable for later recognition
        elif ES or es is True:                                                 # if .EPOS or .epos was selected
            self.label_pos_selected=Label(text='epos file selected')           # creating label for epos
            self.canvas_all.create_window(120,95,window=self.label_pos_selected) #put label on canvas
            self.E=1                                                           # set variable for later recognition
        else:                                                                  # if any other filetype was selected
            messagebox.showinfo(title='APT_analyzer',message='select .pos or .epos file. Warning: Notation has to be either .pos /.epos or .POS / .EPOS')
            self.filename=[]                                                   # leave filename empty
            self.E=2                                                           # set variable back to 2

        
    def search_rrng(self):                                                     # function for searching for rrng file
        self.filename2=filedialog.askopenfilename()                            # getting file from search
        S='.RRNG' in self.filename2                                            # checking if .RRNG is in the filename
        s='.rrng' in self.filename2                                            # checking if .rrng is in the filename
        if S or s is True:                                                     # if .RRNG or .rrng was selected
            self.label_rrng_selected=Label(text='.rrng file selected')         # create label for rrng
            self.canvas_all.create_window(280,95,window=self.label_rrng_selected) #placing label on canvas
            self.R=1                                                           # setting variable for later recognition
        else:                                                                  # if no correct file was selected
            messagebox.showinfo(title='APT_analyzer',message='select .rrng file. Warning: Notation has to be either .rrng or .RRNG')
            self.filename=[]                                                   # leaving filename empty
            self.R=2                                                           # set variable back to 2
        
      
    def calculate_tip(self):                                                   # function for reading and converting the pos and rrng file and creating the tip
      if self.E==2:messagebox.showinfo(title='APT_analyzer',message='no file .pos/.epos file selected')   # checking if no  pos/epos file is selected (E=2)
      elif self.R==2:messagebox.showinfo(title='APT_analyzer',message='no file .rrng file selected')    # checking if no  rrng file is selected (R=2)
      else:                                                                    # if pos/epos and rrng file is selected
        with open(self.filename, 'rb') as f:                                   # opening pos/epos data from file1
            data = f.read()                                                    # reading pos/epos data from file1
        data_rrng=self.filename2                                               # reading rrng data from file2
        if self.E==0:pos=apt.read_pos(data)                                    # converting pos data if pos file was selected (E==0)
        elif self.E==1:pos=apt.read_epos(data)                                 # converting epos data if epos file was selected (E==1)
        rrngs=apt.read_rrng(data_rrng)                                         # converting rrng data
        self.tip=apt.label_ions(pos, rrngs)                                    # label ions using apt_importers functions
        self.ele=apt.unique(list(self.tip['comp']))                            # determining how many unique elements in tip using apt_importers functions
        messagebox.showinfo(title='APT_analyzer',message='successfully calculated tip') # message box that calculation has been successfull
        string=['all']                                                         # setting up strings for atom selection combobox
        for i in range (0,len(self.ele)):                                      # loop over all unique elements
            string.append(self.ele[i])                                         # creating strings with all unique elements
        self.data_atom=(string)                                                # data for combobox containing all unique elements + 'all' at start
        self.cb_atom = Combobox(tk, values=self.data_atom)                     # creating combobox with unique elements data 
        self.canvas_all.create_window(280,235,window=self.cb_atom)             # putting combobox with element selection on canvas
        self.cb_atom.current(0)                                                # setting initial value of combobox to 'all'  

        
    def clear(self):                                                           # function for clearing canvas
        self.fig.clear()                                                       # clearing canvas
        self.canvas.draw_idle()                                                # drawing 
        self.canvas_all.delete('message')                                      # deleting message about concentration data
        
    def plot_tip(self):                                                        # function about plotting tip
        self.canvas_all.delete('message')                                      # clearing message about concentration data
        Z= self.cb_atom.get()                                                  # getting variable from combobox of atom selection
        M = self.slider_res.get()                                              # getting variable from combobox of resolution selection
        SS=self.slider_size.get()                                              # getting variable from combobox of atom size selection
        S=float(SS)/10                                                         # transforming entry into float and deviding by 10 so values 0.1 to 1 are also included
        u_ele=self.ele
        if self.var_plot.get()==0:                                             # checking if plot_single or plot_all was selected
            self.fig.clear()                                                   # if plot single was selected clear all previous plots
            self.ax=self.fig.add_subplot(111,projection='3d')                  # make new figure with full size (111)
        else: self.ax=self.fig.add_subplot(221,projection='3d')                # if plot_all was selected make plot on a 2x2 plot in the first position (221)
        n=len(np.array(self.tip['x']))                                         # get the number of atoms
        N=int(5*n/(int(M)**2*1000))                                            # convert the resolution selection in dependance of the number of total atoms
        x=np.array(self.tip['x'])[::N]                                         # select x cooridant (only take every Nth atom to plot later)
        y=np.array(self.tip['y'])[::N]                                         # select y cooridant from tip data
        z=np.array(self.tip['z'])[::N]                                         # select z cooridant from tip data
        c=np.array(self.tip['colour'])[::N]                                    # select the colour column in the tip data
        label=np.array(self.tip['comp'])[::N]                                  # select the composition column in the tip data
        for i in range(0,len(u_ele)):                                          # loop that goes over every different elements
             e=label==u_ele[i]                                                 # seperation of the elements
             x_new=x[e]                                                        # select the x values of each element indiviually
             y_new=y[e]
             z_new=z[e]
             c_new=c[e]
             if self.i_plot.get()==1:                                          # if inverse tip is selected
                    z_new=-z_new                                               # change the sign of the z coordinates
             if Z=='all':                                                      # if all was selected plot all of them together
                 self.ax.scatter3D(x_new,y_new,z_new,c=c_new,label=u_ele[i],s=S)  # scatter plot each element seperatly and assign label
                 x_N=len(x)                                                    # assigne x_N value to show the number of plotted atoms in title
             elif u_ele[i]==Z:                                                 # if a certain element was selected in combobox for element selection
                 self.ax.scatter3D(x_new,y_new,z_new,c=c_new,label=u_ele[i],s=S)  #scatter plot each element seperatly and assign label         
                 x_N=len(x_new)                                                # assigne x_N only to show the number of plotted atoms of selected element 
        apt.set_axes_equal(self.ax)                                            # function for setting the axes equal for 3d plot
        self.ax.legend()                                                       # show legends of each element
        if self.var_axis.get()==0:                                             # if show axis was selected
            self.ax.set_title('number of atoms=%i' %x_N)                       # show number of atoms plotted in title
            self.ax.set_xlabel('X-axis',fontweight='bold')                     # label x axis
            self.ax.set_ylabel('Y-axis',fontweight='bold')                     # label y axis
            self.ax.set_zlabel('Z-axis',fontweight='bold')                     # label z axis
        elif self.var_axis.get()==1:                                           # if show axis was not selected
            self.ax.set_axis_off()                                             # dont show axis
        
        if self.var_cyl.get()==1:                                              # if show clyinder was selected
             x_pos = float(self.cly_x.get())                                   # get x value from x entry box
             y_pos = float(self.cly_y.get())                                   # get y value from y entry box
             z_pos = float(self.cly_z.get())                                   # get z value from z entry box
             height = float(self.height.get())                                 # get height value from height entry box
             alpha = float(self.alpha.get())                                   # get tilt along y value from alpha entry box
             beta = float(self.beta.get())                                     # get tilt along x value from beta entry box
             r = float(self.radius.get())                                      # get radius value from radius entry box
             color_zyl=str(self.cb_color.get())                                # get color of cylinder from color entry box
             theta=np.linspace(0,2*np.pi,201)                                  # create linspace variable for plotting the circle
             alpha=math.radians(alpha)                                         # transform alpha from deg in rad
             beta=math.radians(beta)                                           # transfrom beta from deg in rad
        
      ########## plotting the cylinder ############################## 
             y_circle=r*np.cos(theta)                               
             x_circle=r*np.sin(theta)
             z_circle_s=np.ones(201)*-height/2
             z_circle_e=np.ones(201)*height/2
             y_circle_rs=y_circle*np.cos(alpha)-z_circle_s*np.sin(alpha)
             z_circle_rs=y_circle*np.sin(alpha)+z_circle_s*np.cos(alpha)
             y_circle_re=y_circle*np.cos(alpha)-z_circle_e*np.sin(alpha)
             z_circle_re=y_circle*np.sin(alpha)+z_circle_e*np.cos(alpha)
             
             x_circle_rs=x_circle*np.cos(beta)+z_circle_rs*np.sin(beta)
             z_circle_rs2=-x_circle*np.sin(beta)+z_circle_rs*np.cos(beta)
             x_circle_re=x_circle*np.cos(beta)+z_circle_re*np.sin(beta)
             z_circle_re2=-x_circle*np.sin(beta)+z_circle_re*np.cos(beta)
             
             x_line1=np.ones(201)*r
             x_line2=np.ones(201)*-r
             y_line=np.ones(201)*0
             z_line=np.linspace(-height/2,height/2,201)

             y_liner=y_line*np.cos(alpha)-z_line*np.sin(alpha)
             z_liner=y_line*np.sin(alpha)+z_line*np.cos(alpha)
             
             x_liner1=x_line1*np.cos(beta)+z_liner*np.sin(beta)
             z_liner2_1=-x_line1*np.sin(beta)+z_liner*np.cos(beta)
             x_liner2=x_line2*np.cos(beta)+z_liner*np.sin(beta)
             z_liner2_2=-x_line2*np.sin(beta)+z_liner*np.cos(beta)
             
             lw=5
             self.ax.plot(x_liner1+x_pos,y_liner+y_pos,z_liner2_1+z_pos,color_zyl,linewidth=lw)
             self.ax.plot(x_liner2+x_pos,y_liner+y_pos,z_liner2_2+z_pos,color_zyl,linewidth=lw)
             self.ax.plot(x_circle_rs+x_pos,y_circle_rs+y_pos,z_circle_rs2+z_pos,color_zyl,linewidth=lw)  
             self.ax.plot(x_circle_re+x_pos,y_circle_re+y_pos,z_circle_re2+z_pos,color_zyl,linewidth=lw)
        self.canvas.draw_idle()
     
        
    def calc_con(self):                                                        # function for calculating the concentration
        self.canvas_all.delete('message')   
        Z= self.cb_atom.get()
        u_ele_real=self.ele
        if self.var_plot.get()==0:
            self.fig.clear()
            self.spec=gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[4,1],wspace=0.5,hspace=0.5,height_ratios=[4,1]) #adjust the size of the figure compared to (111)
            self.ax1=self.fig.add_subplot(self.spec[0])
        else: self.ax1=self.fig.add_subplot(222)  
        self.ax1.set_xlabel('z position of cylinder')
        self.ax1.set_ylabel('concentration [%]')
        x_real=np.array(self.tip['x'])
        y_real=np.array(self.tip['y'])
        z_real=np.array(self.tip['z'])
        c_real=np.array(self.tip['colour'])
        label_real=np.array(self.tip['comp'])
        inter=float(self.slider_inter.get()/20)
        height = float(self.height.get())
        alpha = float(self.alpha.get())
        beta = float(self.beta.get())
        r = float(self.radius.get())
        x_pos = float(self.cly_x.get())
        y_pos = float(self.cly_y.get())
        z_pos = float(self.cly_z.get())
        z_start=-height/2
        z_end=height/2
        alpha=math.radians(alpha)
        beta=math.radians(beta)
        ###################   tilt and move cylinder ######################################
        x_real=x_real-x_pos
        y_real=y_real-y_pos
        z_real=z_real-z_pos
        y_real2=y_real*np.cos(alpha)-z_real*np.sin(alpha)
        z_real2=y_real*np.sin(alpha)+z_real*np.cos(alpha)
        x_real3=x_real*np.cos(beta)+z_real2*np.sin(beta)
        z_real3=-x_real*np.sin(beta)+z_real2*np.cos(beta)
        y_real=y_real2
        x_real=x_real3
        z_real=z_real3
        ##########################################################################
       
        xy=((x_real)**2+(y_real)**2)**(1/2)                                    # cirlce constraint for atoms       
        circle=xy<=r                                                           # only select atoms inside of circle
        message='concentration: \n'                                            # initialize the message displayed on the right side of the plot
        for m in range(0,len(u_ele_real)):                                     # loop over each individual elements
            plot_z=[]                                                          # x component of concentration plots 
            Num=[]                                                             # Number of atoms inside the circle and intervals (for concentration calculation)
            Num_all=[]                                                         # total number of atoms (of each element) to calculate the % contribution of each
            
            e=label_real[circle]==u_ele_real[m]                                # seperation of the elements
            z_circle=z_real[circle]                                            # only selec the atoms with circle constraint
            z_p=z_circle[e]                                                    # only select the atoms wth circle constraint of specific element
            c_circle=c_real[circle]
            c_p=c_circle[e]
            for j in range (0,int((z_end-z_start)/inter)):                     # loop of intervals
                init=z_p>=z_start+j*inter                                      # starting condition of interval for each element
                init_all=z_circle>=z_start+j*inter                             # starting condition of interval for all elements together
                z_all2=z_circle[init_all]                                      # selecting atoms which fulfill starting constraint for all elements
                z_p2=z_p[init]                                                 # selecting atoms which fulfill the starting constraint for each individual element
                init2=z_p2<=z_start+(j*inter+inter)                            # ending constraint of interval
                init2_all=z_all2<=z_start+(j*inter+inter)                      # ending constraint of interval for all elements
                z_all3=z_all2[init2_all]                                       # selecting atoms which also fulfill ending constraint for all elements
                z_p3=z_p2[init2]                                               # selecting atom which also fulfill ending constraint for each individual elements
                Num_all.append(len(z_all3))                                    # append the number of atoms which fulfill both contraints
                Num.append(len(z_p3))                                          # append the number of atoms which fulfill both constraints for each individual element
                plot_z.append(z_start+j*inter+inter/2)                         # append the x-coordinate for the concentration plot
            a=np.array(Num,dtype=float)                                        # transform total number of atoms for each individual element into array of floats
            b=np.array(Num_all,dtype=float)                                    # transform total number of atoms into array of floats
            conc=100*np.divide(a,b, out=np.zeros_like(a), where=b!=0)          # calculate concentration, if total amount of atoms == 0, result is 0
            message=message+u_ele_real[m]                                      # append element type into message
            message=message+': maximal value: '                                # add text to message
            message=message+str(round(max(conc),2))                            # add maximum of concentration to message
            message=message+' minimal value: '                                 # add text to message
            message=message+str(round(min(conc),2))                            # add minimum of concentration to message
            message=message+'\n'                                               # add line split to message
            if Z=='all':                                                       # seperate if atom select checkbox 'all' is selected
                self.ax1.plot(plot_z,conc,c_p[0],label=u_ele_real[m])                 # plot the concentration of each element individually
            elif u_ele_real[m]==Z:                                             # if certain element is selected in checkbox
                self.ax1.plot(plot_z,conc,c_p[0],label=u_ele_real[m])                 # only plot selected element from the select atom checkbox
        self.ax1.legend()
        self.ax1.set_title('concentration of elements along cylinder / intervalsize=%1.2f' %inter)
        self.canvas.draw_idle()
        self.message=Message(text=message,bg='white')#,relief=SUNKEN)
        self.message.config(width=300)#font=('times',12))
        self.canvas_all.create_window(1300,500,window=self.message,tags='message')
        
        
        
        
    def calc_excess(self):
        self.canvas_all.delete('message')   
        if self.var_plot.get()==0:
            self.fig.clear()
            self.spec=gridspec.GridSpec(ncols=2,nrows=2,width_ratios=[4,1],wspace=0.5,hspace=0.5,height_ratios=[4,1])
            self.ax3=self.fig.add_subplot(self.spec[0])
        else: self.ax3=self.fig.add_subplot(224)
        self.ax3.set_xlabel('z position of cylinder')
        self.ax3.set_ylabel('Total amount of atoms')
        Z= self.cb_atom.get()
        u_ele_real=self.ele
        x_real=np.array(self.tip['x'])
        y_real=np.array(self.tip['y'])
        z_real=np.array(self.tip['z'])
        c_real=np.array(self.tip['colour'])
        label_real=np.array(self.tip['comp'])
        inter=float(self.slider_inter.get()/20)
        height = float(self.height.get())
        alpha = float(self.alpha.get())
        beta = float(self.beta.get())
        r = float(self.radius.get())
        x_pos = float(self.cly_x.get())
        y_pos = float(self.cly_y.get())
        z_pos = float(self.cly_z.get())
        z_start=-height/2
        z_end=height/2
        alpha=math.radians(alpha)
        beta=math.radians(beta)
        ###################   tilt and move zylinder ######################################
        x_real=x_real-x_pos
        y_real=y_real-y_pos
        z_real=z_real-z_pos
        y_real2=y_real*np.cos(alpha)-z_real*np.sin(alpha)
        z_real2=y_real*np.sin(alpha)+z_real*np.cos(alpha)
        x_real3=x_real*np.cos(beta)+z_real2*np.sin(beta)
        z_real3=-x_real*np.sin(beta)+z_real2*np.cos(beta)
        y_real=y_real2
        x_real=x_real3
        z_real=z_real3
        ##########################################################################
        
        xy=((x_real)**2+(y_real)**2)**(1/2)
        circle=xy<=r

        for m in range(0,len(u_ele_real)):
            Num_sum=[]
            plot_z=[]
            Num_s=0
            e=label_real[circle]==u_ele_real[m]               #seperation of the atoms 
            z_circle=z_real[circle]
            z_p=z_circle[e]
            c_circle=c_real[circle]
            c_p=c_circle[e]
            
            for j in range (0,int((z_end-z_start)/inter)):
                init=z_p>=z_start+j*inter   
                z_p2=z_p[init]
                init2=z_p2<=z_start+(j*inter+inter)
                z_p3=z_p2[init2]
                Num_s=Num_s+len(z_p3)
                Num_sum.append(Num_s)
                plot_z.append(z_start+j*inter+inter/2)   
            c=np.array(Num_sum,dtype=float)
            if Z=='all':
                self.ax3.plot(plot_z,c,c_p[0],label=u_ele_real[m])
            elif u_ele_real[m]==Z:
                self.ax3.plot(plot_z,c,c_p[0],label=u_ele_real[m]) 
        self.ax3.set_title('total atom number of elements along cylinder / intervalsize=%1.2f ' %inter)
        self.ax3.legend()
        self.canvas.draw_idle()  
        
            
    def calc_zoom(self):     
        self.canvas_all.delete('message')   
        if self.var_plot.get()==0:
            self.fig.clear()
            self.ax2=self.fig.add_subplot(111,projection='3d')
        else: self.ax2=self.fig.add_subplot(223,projection='3d')
        Z= self.cb_atom.get()
        M = self.slider_res.get()
        SS=self.slider_size.get()
        S=float(SS)/10
        u_ele_real=self.ele
        n=len(np.array(self.tip['x']))
        N_plot=int(n/(int(M)**2*1000))
        x_real=np.array(self.tip['x'])
        y_real=np.array(self.tip['y'])
        z_real=np.array(self.tip['z'])
        c_real=np.array(self.tip['colour'])
        label_real=np.array(self.tip['comp'])
        height = float(self.height.get())
        alpha = -float(self.alpha.get())
        beta = -float(self.beta.get())
        r = float(self.radius.get())
        x_pos = float(self.cly_x.get())
        y_pos = float(self.cly_y.get())
        z_pos = float(self.cly_z.get())
        color_zyl=str(self.cb_color.get())
        z_start=-height/2
        z_end=height/2
        alpha=math.radians(alpha)
        beta=math.radians(beta)
        
        ###################   tilt and move zylinder ######################################
        x_real=x_real-x_pos
        y_real=y_real-y_pos
        z_real=z_real-z_pos
        y_real2=y_real*np.cos(alpha)-z_real*np.sin(alpha)
        z_real2=y_real*np.sin(alpha)+z_real*np.cos(alpha)
        x_real3=x_real*np.cos(beta)+z_real2*np.sin(beta)
        z_real3=-x_real*np.sin(beta)+z_real2*np.cos(beta)
        y_real=y_real2
        x_real=x_real3
        z_real=z_real3
        #########################################################################  
        xy=((x_real)**2+(y_real)**2)**(1/2)
        circle=xy<=r
        for m in range(0,len(u_ele_real)):
            e=label_real[circle]==u_ele_real[m]               #seperation of the atoms 
            z_circle=z_real[circle]
            x_circle=x_real[circle]
            y_circle=y_real[circle]
            c_circle=c_real[circle]
            z_p=z_circle[e]  
            x_p=x_circle[e] 
            y_p=y_circle[e]
            c_p=c_circle[e]
            init_plot=z_p>=z_start
            x_pl2=x_p[init_plot]
            y_pl2=y_p[init_plot]
            z_pl2=z_p[init_plot]
            c_pl2=c_p[init_plot]
            init_plot2=z_pl2<=z_end    
            x_pl3=x_pl2[init_plot2]
            y_pl3=y_pl2[init_plot2]
            z_pl3=z_pl2[init_plot2]
            c_pl3=c_pl2[init_plot2]
            if Z=='all':
                self.ax2.scatter3D(x_pl3[::N_plot],y_pl3[::N_plot],z_pl3[::N_plot],c=c_pl3[::N_plot],label=u_ele_real[m],s=S)
                x_N=len(x_real[::N_plot])
            elif u_ele_real[m]==Z:
                self.ax2.scatter3D(x_pl3[::N_plot],y_pl3[::N_plot],z_pl3[::N_plot],c=c_pl3[::N_plot],label=u_ele_real[m],s=S)
                x_N=len(x_pl3[::N_plot])
                      
        if self.var_axis.get()==0: 
            self.ax2.set_title('number of atoms=%i' %x_N)
            self.ax2.set_xlabel('X-axis',fontweight='bold')
            self.ax2.set_ylabel('Y-axis',fontweight='bold')
            self.ax2.set_zlabel('Z-axis',fontweight='bold')
        elif self.var_axis.get()==1:
            self.ax2.set_axis_off()   
            
        apt.set_axes_equal(self.ax2)   
        self.ax2.legend() 
        if self.var_cyl.get()==1:
            x_pos = float(self.cly_x.get())
            y_pos = float(self.cly_y.get())
            z_pos = float(self.cly_z.get())
            height = float(self.height.get())
            alpha = float(self.alpha.get())
            beta = float(self.beta.get())
            r = float(self.radius.get())
            color_zyl=str(self.cb_color.get())
            theta=np.linspace(0,2*np.pi,201)
            z_start=-height/2
            z_end=height/2
            alpha=math.radians(alpha)
            beta=math.radians(beta)
        
            y_circle=r*np.cos(theta)
            x_circle=r*np.sin(theta)
            z_circle_s=np.ones(201)*z_start
            z_circle_e=np.ones(201)*z_end

            x_line1=np.ones(201)*r
            x_line2=np.ones(201)*-r
            y_line=np.ones(201)*0
            z_line=np.linspace(z_start,z_end,201)
            lw=5
            self.ax2.plot(x_line1,y_line,z_line,color_zyl,linewidth=lw)
            self.ax2.plot(x_line2,y_line,z_line,color_zyl,linewidth=lw)
            self.ax2.plot(x_circle,y_circle,z_circle_s,color_zyl,linewidth=lw)  
            self.ax2.plot(x_circle,y_circle,z_circle_e,color_zyl,linewidth=lw) 
        self.canvas.draw_idle() 

tk = Tk()                                                                      # tkinter
tk.title("APT analyzer")                                                       # select title of tool
tk.geometry('1100x700')                                                        # select size of tool
tt=APT_analyzer(tk)                                                            # select tool              
tk.mainloop()                                                                  # start tool