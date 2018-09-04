import matplotlib.pyplot as plt
from math import exp


def get_samples(mem_mtbf, n=60):
    lambda_cpu = 1 / 9  # 1 / MTBF_cpu
    lambda_mem = 1 / mem_mtbf  # 1 / MTBF_mem

    # R(t) = e^-λt -> per module
    def Rcpu_fn(t): return exp(-lambda_cpu * t)

    def Rmem_fn(t): return exp(-lambda_mem * t)

    def R1_fn(t): return 2 * Rcpu_fn(t) * Rmem_fn(t) - \
        Rcpu_fn(t) ** 2 * Rmem_fn(t) ** 2

    def R2_fn(t): return (2 * Rcpu_fn(t) - Rcpu_fn(t) ** 2) * \
        (2 * Rmem_fn(t) - Rmem_fn(t) ** 2)

    # Exponential CDF: F(t) = 1 - R(t)
    def F1_fn(t): return 1.0 - R1_fn(t)

    def F2_fn(t): return 1.0 - R2_fn(t)

    t = range(n)
    F1, F2 = list(map(F1_fn, t)), list(map(F2_fn, t))
    return (F1, F2)


# fig = plt.figure()
# ax = fig.add_subplot(111)
# F1, F2 = get_samples(6)
# line1, = ax.plot(F1, label="F1")
# line2, = ax.plot(F2, label="F2")
# plt.title("Exponential CDF")
# plt.ylabel("F(t)")
# plt.xlabel("t")
# plt.ion()
# plt.show()

for mtbf in range(1, 600000):
    F1, F2 = get_samples(mtbf)

    # Count how many samples of F1 that has lower failure rates
    cntr = 0
    for f1, f2 in zip(F1, F2):
        cntr += 1 if f1 < f2 else 0
    print(f"Mem MTBF = {mtbf}, {cntr} samples have lower failure rates")

    # line1.set_ydata(F1)
    # line2.set_ydata(F2)
    # plt.pause(1e-2)
