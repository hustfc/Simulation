import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'font.size': 16}) 




plt.xlabel('round')
plt.xlim(0,20)
plt.ylim(0,1)
plt.ylabel('fairness')
cicle = [i for i in range(0,20)]
game_fair = [0, 0.05, 0.1, 0.15, 0.15, 0.2, 0.2, 0.25, 0.3, 0.35, 0.4, 0.4, 0.45, 0.45,
              0.49999725808766626, 0.5490915372696149, 0.5494345676331145, 0.5986329518439101, 0.6434627526049957]
plt.plot(cicle,game_fair)              
plt.legend()
plt.show()