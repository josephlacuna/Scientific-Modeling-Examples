import matplotlib.pyplot as plt
import numpy as np

P=np.linspace(0.7,4.0,100000)
m=0.7
# Initialize your data containers identically
X = []
Y = []
# l is never used, I removed it.
for u in P:
    # Add one value to X instead of resetting it.
    X.append(u)
    # Start with a random value of m instead of remaining stuck
    # on a particular branch of the diagram
    m = np.random.random()
    for n in range(1001):
      m=(u*m)*(1-m)
    # The break is harmful here as it prevents completion of
    # the loop and collection of data in Y
    for l in range(1051):
      m=(u*m)*(1-m)
    # Collection of data in Y must be done once per value of u
    Y.append(m)
# Remove the line between successive data points, this renders
# the plot illegible. Use a small marker instead.
plt.scatter(X, Y, marker=',', color = 'k', s = 1)
#plt.axvline(x=2.9974, color = 'r')
#plt.axvline(x=3.4486, color = 'r')
#plt.axvline(x=3.4495, color = 'r')
#plt.axvline(x=3.5446, color = 'r')
#plt.axvline(x=3.5652, color = 'r')
plt.xlim(0.7,4.05)
plt.ylim(-0.05,1.05)
plt.xlabel("Growth Parameter [r]")
plt.ylabel("x")
plt.title("Logistic Map")
plt.savefig('logistic_map0.png', dpi = 1024, bbox_inches = 'tight')
plt.close()
