#!/usr/bin/env python

"""

mcworldgen.py

Standalone generator for mcworldgen: generates a default-ish minecraft map.

"""


# Dependencies
import random
import math
import copy
import time
import os
import subprocess
import numpy
import time
import pymclevel as mcl
import sys

# Modules to test
from diamondsquare import *
from layer import *
from landmark import *
from saveutils import *

def namedModule(name):
    """Return a module given its name."""
    try:
        topLevel = __import__(name)
    except ImportError:
        name = "pipelines."+name
        topLevel = __import__(name)
    packages = name.split(".")[1:]
    m = topLevel
    for p in packages:
        m = getattr(m, p)
    return m

random.seed()

def filtertest(modulename="default"):
    totaltime = 0

    testworld = createWorld("nuclai.world")
    # cool seeds: 12397
    worldseed = random.randint(0, 65535)
    worldsizex = 8
    worldsizez = 8
    print("World seed is", worldseed)
    
    pipeline = namedModule(modulename)
    tfilter = pipeline.build(worldseed, testworld)

    # Generate minecraft level
    for chunkrow in range(-worldsizex, worldsizex):
        print("Generating chunk ", chunkrow)

        for chunkcol in range(-worldsizez, worldsizez):
            #print "\n========\nChunk", (chunkrow, chunkcol), "\n========"   
            
            starttime = time.clock()     
            currchunk = tfilter.getChunk(chunkrow, chunkcol)
            endtime = time.clock()
            totaltime += endtime - starttime
            setWorldChunk( testworld, currchunk, chunkrow, chunkcol)
    
    saveWorld(testworld)
    # renderWorld("testworld", "testworld-"+str(worldseed)+"-"+str(worldsizex*2)+"x"+str(worldsizez*2))

    print("Processing took", totaltime, "seconds.")

if __name__ == "__main__":
    if not os.path.isdir("output"):
        os.mkdir("output")
    
    if len(sys.argv)>1:
        filtertest(sys.argv[1])
    else:
        filtertest()
    
    print("Generation complete.")

