#==================================
# Importing required modules
#==================================

import numpy as np
import scipy as sc
import math
import matplotlib.pyplot as plt


#==================================
# 1D input
#==================================

def oneD(d):
    print("a visual neuron's temporal response")

    k = 25 # Temporal sscale factor
    n = 5
    t= np.linspace(0, 1, 50)
    slow_t = np.power((k*t),n) * np.exp(-k*t)*(1/sc.math.factorial(n)-np.power((k*t),2)/sc.math.factorial(n+2))

    n = 3
    fast_t = np.power((k*t),n) * np.exp(-k*t)*(1/sc.math.factorial(n)-np.power((k*t),2)/sc.math.factorial(n+2))

    b = slow_t + fast_t #linear filter
    c=np.convolve(b,d) # convolve filter with stimulus
    d=c/np.max(c) # normalize

    e=100./(1.0 + np.exp(10*(0.5-d))) # static nonlinearity
    r=e #for continuous output

    return r



white_noise = np.random.uniform(-1, 1, 1000)
print(white_noise)

temporal_response = oneD(white_noise)
print(temporal_response)

linear_filter = np.correlate(white_noise, temporal_response)
print(len(linear_filter))

normal_filter = linear_filter/np.power((np.std(white_noise)),2) * len(white_noise)

estimated_output = np.convolve(white_noise, normal_filter)

plt.plot(normal_filter)
plt.show()

plt.scatter(temporal_response, estimated_output)
plt.show()


#==================================
# 3D input
#==================================

def threed(a):
  print("simulating a V1 simple cell's spatiotemporal response") 
  siz=a.shape
  x=siz[0]
#   y=siz[1]
  z=siz[2]
  SIZE=x
  SF=0.15
  SIG=7
  OR=90*math.pi/180
  AR=3
  PH=0

  k=25  #Temporal scale factor 
  n=5
  t = np.linspace(0,1,50)
  slow_t=np.power((k*t),n) * np.exp(-k*t)*(1/sc.math.factorial(n)-np.power((k*t),2)/sc.math.factorial(n+2))

  n = 3
  fast_t=np.power((k*t),n) * np.exp(-k*t)*(1/sc.math.factorial(n)-np.power((k*t),2)/sc.math.factorial(n+2))

  b = slow_t + fast_t # linear filter

  xx = np.linspace(1, SIZE, SIZE)
  xdata,ydata=np.meshgrid(xx,xx)
  temp1=(xdata-SIZE/2)*math.cos(OR)+(np.matrix.transpose(xdata)-SIZE/2)*np.sin(OR)
  temp2=(-xdata+SIZE/2)*math.sin(OR)+(np.matrix.transpose(xdata)-SIZE/2)*np.cos(OR)

  f1 = np.exp(-(np.multiply(temp1,temp1) + AR*AR*np.multiply(temp2,temp2)) / (2*SIG*SIG))
  f2 = np.cos(2*np.pi*SF*temp2+PH)
 
  rf_image = np.multiply(f1,f2)
  rf_image = rf_image - np.mean(rf_image)
  dp=[0]*(z)
  for ii in range (0,z-1,1):
    dp[ii]=np.sum(np.multiply(a[:,:,ii],rf_image))

  c=np.convolve(b,dp) # convolve filter with stimulus
  c=c/np.max(c) # normalize
  
  c[np.where(c<0)]=0

  r=c
  r[np.where(r>0.4)]=1 #spiking binary output
  r[np.where(r<=0.4)]=0
   
  return(r)
