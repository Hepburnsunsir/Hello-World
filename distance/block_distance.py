#!/usr/bin/env python3

import argparse
import networkx as nx
import json

#calculate function level distance
def call_distance():
  for node in CG.nodes():
    #print("node {}\n".format(node))
    d = 0  # unreachable
    i = 0
    for t in tfuncs:
        try:
          shortest = nx.dijkstra_path_length (CG, node,t )
          d += 1.0 / (1.0 + shortest)
          i += 1
        except nx.NetworkXNoPath:
          pass
    if d != 0:
      d = i/d
      cg_distance[node]=d
      #out.write (str(node))
      #out.write (",")
      #out.write (str (d))
      #out.write ("\n")   

## Calculate basic block level distance
def block_distance ( ):
  for node in CFG.nodes():
    d = 0
    i = 0 
    if node in bb_distance.keys():
      d = 10 * bb_distance[node]
      bout.write (str(node))
      bout.write (",")
      bout.write (str(d))
      bout.write ("\n")
      continue
    else: 
        for t_name, bb_d in bb_distance.items():
          #if G.has_node(t_name):
            try:
              shortest = nx.dijkstra_path_length(CFG, node, t_name)
              d += 1.0 / (1.0 + 10 * bb_d + shortest)
              i += 1
            except nx.NetworkXNoPath:
              pass
    if d != 0 :
      d = i/d
      bout.write (str(node))
      bout.write (",")
      bout.write (str(d))
      bout.write ("\n")
    
      
# Main function
if __name__ == '__main__':
  parser = argparse.ArgumentParser ()
  parser.add_argument ('-j', '--json', type=str, required=True, help="Path to json-file representing the control flow graph and call graph.")
  parser.add_argument ('-tb', '--target_blocks', type=str, required=True, help="Path to file specifying Target blocks.")
  parser.add_argument ('-tf', '--target_functions', type=str, required=True, help="Path to file specifying Target functions.")
  #parser.add_argument ('-of', '--out_functions', type=str, required=True, help="Path to output file containing distance for each function.")
  parser.add_argument ('-ob', '--out_blocks', type=str, required=True, help="Path to output file containing distance for each block.")
  args = parser.parse_args ()

  print ("\n Parsing %s .." % args.json)
  cgcfg = {}
  with open(args.json, "r") as f:
    cgcfg =  json.load(f) 

  #build call graph in a binary, CG means call graph for functions in a binary
  CG = nx.DiGraph()
  for key, value in cgcfg.items():
    CG.add_node(key, name = value['name'])
    for ckey in value['call']:
        CG.add_edge(key, ckey[2])
  
  print(nx.info(CG))
  print(CG.nodes(), CG.edges())
  
  
  cg_distance={}  
  tfuncs = set()

  print("\ntarget function\n") 
  with open(args.target_functions,"r") as ft:
    for line in ft.readlines():
      tfuncs.add(line.strip())
      print(line.strip())
 
  #with open(args.out, "w") as out:
      #call_distance ()
  call_distance()

  print("\ncall graph cg_distance\n")
  for key, value in cg_distance.items() :
    print ( key , value )
  
  
  CFG = nx.DiGraph()
  bb_distance = {}
  tblocks = set()

  print("\n target blocks\n")
  with open(args.target_blocks,"r") as fb:
    for line in fb.readlines():
      tblocks.add(line.strip())
      print(line.strip())
  

  for key, value in cgcfg.items():
    CFG.clear()
    bb_distance.clear()
    print ("calculate cfg_distance for function '%s', '%s'.. " % (value['name'],key))
    # add basic block 
    for b in value['block']:
      CFG.add_node(b[0])

    #chech and add target basic block
    for i in tblocks:
      if CFG.has_node(i):
        bb_distance[i] = 0
    # add edge
    for e in value['jmp']:
      CFG.add_edge(e[0], e[1])

    # add blocks that can reach target function
    for c in value['call']:
      if c[2] in cg_distance.keys():
        if c[0] in bb_distance.keys():
            if bb_distance[c[0]] > cg_distance[c[2]]:
                bb_distance[c[0]] = cg_distance[c[2]]
        else:
            bb_distance[c[0]] = cg_distance[c[2]]
    
    print("blocks reach targets ")
    for key , value in bb_distance.items():
      print (key , value)

    with open(args.out_blocks, "a") as bout:
      block_distance()


    
        