# from scipy.optimize import differential_evolution
# def f(x):
#     return 1/x
#
# bound = 0.1
# result = differential_evolution(f,[(-bound,bound)],disp=True, maxiter=1000)
# print(result)

from matplotlib import pyplot as plt
lines = [line.rstrip('\n') for line in open('newWeightsPlotSmallBound3times4NOy')]
print(lines[0:5])
runs = [x.split(",")[0] for x in lines]
scores = [x.split(",")[1] for x in lines]
# plt.scatter(runs, scores,marker=2)
# plt.show()

avg = []
avgs = []
for i in range(len(scores)):
    score = float(scores[i])
    if len(avg) < 2000:
        avg.append(score)
    else:
        avg.pop(0)
        avg.append(score)
    avgs.append(sum(avg)/len(avg))

plt.plot(range(len(avgs)),avgs)
plt.show()