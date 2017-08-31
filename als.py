#!/usr/bin/env

import numpy

def als(R, K, steps = 15, beta = 0.0002):
    M, N = R.shape
    print M, N
    X = numpy.random.rand(M, K)
    X = numpy.mat(X)
    Y = numpy.random.rand(N, K)
    Y = numpy.mat(Y)
    I = numpy.mat(numpy.eye(K))

    err = list()
    it  = list()
    for step in xrange(steps):
        X1 = list()
        Y1 = list()

        P = (Y.T * Y + beta * I).I * Y.T
        for i in xrange(M):
            X1.append([j[0,0] for j in (P * R[i, :].T)])
        print len(X1), len(X1[0])
        raw_input()
        X = numpy.mat(X1)

        Q = (X.T * X + beta * I).I * X.T
        for i in xrange(N):
            Y1.append([j[0,0] for j in (Q * R[:, i])])
        print len(Y1), len(Y1[0])
        raw_input()
        Y = numpy.mat(Y1)

        it.append(step)
        err_ = numpy.sqrt(numpy.sum(pow(numpy.array(R - X * Y.T), 2)) / (M * N))
        print err_
        raw_input()
        err.append(numpy.sqrt(numpy.sum(pow(numpy.array(R - X * Y.T), 2)) / (M * N)))
    return it, err

if __name__ == "__main__":
    M = 1000
    F = 30
    U = 3000
    R = numpy.matrix(numpy.random.rand(M, F)) * numpy.matrix(numpy.random.rand(U, F)).T

    it, err1 = als(R, F, beta=0.1)
    #it, err2 = als(R, F, beta=0.01)
    #it, err3 = als(R, F, beta=0.001)
    #it, err4 = als(R, F, beta=0.0001)

    exit(0)
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(it, err1, 'r', label='beta=0.1')
    ax.plot(it, err2, 'b', label='beta=0.01')
    ax.plot(it, err3, 'y', label='beta=0.001')
    ax.plot(it, err4, 'g', label='beta=0.0001')
    ax.legend(loc='upper right')
    plt.xlabel('iterations')
    plt.ylabel('rsme')
    plt.show()
