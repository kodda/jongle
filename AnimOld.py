import Tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sw

class Ball(object):
    def __init__(self,jugg,hand,col):
        self.t=0
        self.x=250+hand*100        
        self.y=500 
        self.hand=hand 
        self.throw=0       
        self.t_flight=0
	self.im = jugg.create_oval(self.x - 50 , self.y - 50, self.x  , self.y , width=2, fill=col) #ball size=50

    def throw_it(self,throw):
       self.t=0
       self.hand*=-1
       self.throw=throw
       self.t_flight=4*throw-0.5  
       return 0
        
    def update_flight(self,jugg):
       self.t+=0.025
       self.x,self.y=parabola(self)
       jugg.coords(self.im, self.x-50 , self.y-50, self.x ,self.y)
       return 0 

    def update_hand(self,jugg):
       self.t+=0.025
       x_0=250-self.hand*150
       x_1=250-self.hand*100
       self.x=x_0+(x_1-x_0)*(self.t-self.t_flight)/.5
       jugg.coords(self.im, self.x-50 , self.y-50, self.x ,self.y)
       return 0

def parabola(b):
   x_0=250+b.hand*100
   if b.throw%2==0: x_1=250+b.hand*150
   else: x_1=250-b.hand*150 
   x=x_0+(x_1-x_0)*b.t/b.t_flight
   y=500-5.*(b.t_flight*b.t-b.t**2)
   return x,y

#Button functions
def find_patterns():
   global graph,figs_list
   #Drawing the graph and making the figs list
   nb=int(b_entry.get())
   mh=int(mh_entry.get())
   G,figs=sw.graph_and_figs(nb,mh)
   """
   graph_fig=sw.basic_draw(G)
   graph.get_tk_widget().destroy()
   graph = FigureCanvasTkAgg(graph_fig,master=siteswaps)
   graph.show()
   graph.get_tk_widget().grid(row=0,column=0,rowspan=30)
   figs_list.delete(0,Tk.END)
   """
   for fig in figs:
      figs_list.insert(Tk.END,fig)

def jugg_init():
   global balls,nb,hand
   colors=["red","yellow","green","blue","black","white","black","cyan","magenta"]
   for i in range(int(nb.get())):
      balls.append(Ball(jugg,hand,colors[i]))
      hand*=-1

def one_step_init():
   global jugg,t_glob,cur_fig,balls,nb,jballs
   print abs(int(t_glob)-t_glob),"jugglin ball",jballs
      
   #Throwing all balls for the first time
   if abs(t_glob-4*jballs)<0.0001 and jballs<int(nb.get()):
      print t_glob,"jugglin ball",jballs
      balls[jballs].throw=int(cur_fig[0])
      balls[jballs].t_flight=4*balls[jballs].throw-0.5 
      cur_fig=cur_fig[1:]+cur_fig[0]
      jballs+=1
   for b in balls:
      if b.throw>0 and b.t<b.t_flight: b.update_flight(jugg)
      if b.throw>0 and b.t>b.t_flight: b.update_hand(jugg) 
      if b.throw>0 and b.t>b.t_flight+.5:
         b.throw_it(int(cur_fig[0]))     
         cur_fig=cur_fig[1:]+cur_fig[0]
 
   t_glob+=.025
   jugg.after(10,one_step_init)
   return True

def juggle():
   global jugg,t_glob,balls,figs_list,cur_fig,hand,jballs
   hand=-1
   jballs=0
   id_fig=figs_list.curselection()[0]
   cur_fig=figs_list.get(id_fig)
   t_glob=0.
   balls=[]
   jugg_init()
   one_step_init()    

##############
#Windows set##
##############

#parameters 
control_height=100
anim_height=600
anim_width=400
graph_height=300
graph_width=400

G=[]
figs=[]
f=[]

root=Tk.Tk()
root.title("KyoKugei")

anim = Tk.Frame(root)
anim.grid(row=0,  padx =5)

#drawing a juggler
jugg = Tk.Canvas(anim,bg='white',height=anim_height, width=anim_width)
photo = Tk.PhotoImage(file="base_perso2.gif")  
jugg.create_image(250,250,image=photo)
jugg.grid(row = 1 ,rowspan =30 ,  padx =5, pady =5)


siteswaps = Tk.Frame(root)
siteswaps.grid(row=0,column=2)

graph_fig=sw.simple_win()
graph = FigureCanvasTkAgg(graph_fig,master=siteswaps)
graph.show()
graph.get_tk_widget().grid(row=0,column=0,rowspan=30)

control = Tk.Frame(siteswaps, bd=5, relief=Tk.SUNKEN)
control.grid(row=0,column=3)


b_text=Tk.Label(control,text="balls")
nb=Tk.StringVar()
b_entry=Tk.Entry(control,width=2,textvariable=nb)
nb.set(3)
mh_text=Tk.Label(control,text="Max. height")
max_h=Tk.StringVar()
mh_entry=Tk.Entry(control,width=2,textvariable=max_h)
max_h.set(5)
patt_button=Tk.Button(control,text="Find \n patterns",command=find_patterns)
figs_list=Tk.Listbox(master=control)
j_butt=Tk.Button(control,text="Juggle!",command=juggle)


b_text.grid(column=0,row=0)
b_entry.grid(column=0,row=1)
mh_text.grid(column=2,row=0,columnspan=3)
mh_entry.grid(column=2,row=1,columnspan=3)
patt_button.grid(column=1,row=3,rowspan=2,columnspan=2)
figs_list.grid(column=0,row=5,columnspan=4)
j_butt.grid(column=1,row=8,columnspan=2,rowspan=2)

root.mainloop()
