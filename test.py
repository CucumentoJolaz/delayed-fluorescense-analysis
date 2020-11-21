from matplotlib import pyplot as plt
plt.ion()
plt.plot([1,2,3])
# h = plt.ylabel('y')
# h.set_rotation(0)
plt.ylabel(-0.1, 0.5, 'Y label', rotation=90,
            verticalalignment='center', horizontalalignment='right',
            transform=plt.ylabel.transAxes)
plt.draw()