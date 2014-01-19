import numpy as np
import matplotlib.pyplot as pl
import networkx as nx
import cycles_find

#build graph and list figs for b balls with maximum height mh

def build_graph(b,mh,states):
   G=nx.DiGraph()
   for i,s in enumerate(states):
      if s[0]=="0": #no ball coming 
          dest=states.index(s[1:]+"0")
          G.add_weighted_edges_from([(states[i],states[dest],1)])
      else:
          for k in range(1,mh): #testing for collision with throw i
              if (s[k]=="0"):    
                 dest=states.index(s[1:k]+"1"+s[k+1:]+"0")
                 G.add_weighted_edges_from([(states[i],states[dest],k+1)])
              
          dest=states.index(s[1:]+"1")
          G.add_weighted_edges_from([(states[i],states[dest],mh+1)])
   return G    
             
def states_array(nb,mh):
   k=0
   states=[]
   level_generate_states(states,nb,mh,"","0",k)
   level_generate_states(states,nb,mh,"","1",k)
   return states 

def level_generate_states(states,nb,mh,s,next,k):
   s+=next
   if (len(s)==mh) & (s.count("1")==nb ): 
          states.append(s)
          k+=1
   if (len(s)<mh) & (s.count("1")<=nb) :
         level_generate_states(states,nb,mh,s,"0",k)
         level_generate_states(states,nb,mh,s,"1",k)
   else:
      return 0  

def graph_and_figs(b,mh):
   states=states_array(b,mh) 
   G=build_graph(b,mh,states)
   cycles=cycles_find.circuits(G)
   figs=[]
   for c in cycles:
      fig=""
      for i in range(1,len(c)):
         fig+="%d"%(G[c[i-1]][c[i]]['weight']-1)
      figs.append(fig)
   figs.sort(reverse=True)
   return G,figs

def simple_win():
   f = pl.figure(figsize=(5,6))
   a = f.add_subplot(111)
   a.set(xticks=[],yticks=[])
   return f   

def basic_draw(G):
   f = pl.figure(figsize=(5,6))
   a = f.add_subplot(111)
   a.set(xticks=[],yticks=[])
   pos=nx.circular_layout(G)
   nx.draw_networkx_nodes(G,pos,node_size=600,ax=a)
   nx.draw_networkx_labels(G,pos,font_size=9,ax=a)
   nx.draw_networkx_edges(G,pos,ax=a)
   return f
