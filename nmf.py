#!/usr/bin/python
#
# Created by Albert Au Yeung (2010)
#
# An implementation of matrix factorization
#
try:
    import numpy
except:
    print "This implementation requires the numpy module."
    exit(0)

###############################################################################

import pdb, math
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(levelname)s: %(message)s", datefmt='%H:%M:%S'
)

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""


def mf(R, K=20, steps=25, alpha=0.01, beta=0.1):
    logging.info("Parameters for NMF: K=%d, steps=%d, alpha=%f, beta=%f", K, steps, alpha, beta)
    N = len(R)
    M = len(R[0])
    logging.info("Matrix of %d * %d",N,M)

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)

    Q = Q.T
    prevloss = 0
    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (eij * P[i][k] - beta * Q[k][j])
        loss = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    loss += pow((R[i][j] - numpy.asscalar(numpy.dot(P[i, :], Q[:, j]))), 2)
                    pi = 0
                    qj = 0
                    for k in xrange(K):
                        pi += pow(P[i][k], 2)
                        qj += pow(Q[k][j], 2)
                    loss += beta * (pow(pi, 0.5) + pow(qj, 0.5))

        logging.debug("Total loss is %.2f  after %d iterations", loss, step + 1)
        if prevloss != 0 and prevloss - loss < 100:
            logging.info("Converge after %d iterations", step + 1)
            break
        prevloss = loss
    logging.info("Total loss is %.2f", prevloss)
    return P,Q






def bpr(order,M,N, K=20, steps=10, alpha=0.01, beta=0.05,mu=1):
    logging.info("Parameters for BPR: K=%d, steps=%d, alpha=%f, beta=%f", K, steps, alpha, beta)
    logging.info("Matrix of %d * %d",M,N)

    P = mu*numpy.random.rand(M, K)
    Q = mu*numpy.random.rand(N, K)
    Q = Q.T
    for step in xrange(steps):
        for (u,i,j) in order:
            uihat=numpy.dot(P[u, :], Q[:, i])
            ujhat = numpy.dot(P[u, :], Q[:, j])
            P[u,:]=P[u,:]-alpha*(sigmoid(ujhat-uihat)*(Q[:,j]-Q[:,i])-beta*P[u,:])
            Q[:,i]=Q[:,i]-alpha*(-P[u,:]*sigmoid(ujhat-uihat)+beta*Q[:,i])
            Q[:,j]=Q[:,j]-alpha*(P[u,:]*sigmoid(ujhat-uihat)-beta*Q[:,j])

        orderloss=0
        for (u,i,j) in order:
            uihat=numpy.dot(P[u, :], Q[:, i])
            ujhat = numpy.dot(P[u, :], Q[:, j])
            orderloss+=sigmoid(uihat-ujhat)

        regloss=numpy.linalg.norm(P)+numpy.linalg.norm(Q)
        logging.debug("Total loss is %2.f %.2f  after %d iterations", orderloss,numpy.linalg.norm(Q), step + 1)
    return numpy.dot(P, Q)


def cbpr(order,M,N, cap, userp, K=20, steps=10, alpha=0.01, beta=0.05,theta=0.2):
    logging.info("Parameters for BPR: K=%d, steps=%d, alpha=%f, beta=%f", K, steps, alpha, beta)
    logging.info("Matrix of %d * %d",M,N)

    P = numpy.random.rand(M, K)
    Q = numpy.random.rand(N, K)
    Q = Q.T
    reorder={}
    for (u,i,j) in order:
        if j in reorder:reorder[j].append((u,i))
        else: reorder[j]=[(u,i)]
    for step in xrange(steps):

        for j in reorder:
            ej=0
            for t in xrange(M):
                ej += userp[t] * sigmoid(numpy.dot(P[t, :], Q[:, j]))  # calculating E(usage(j))
            for (u,i) in reorder[j]:
                uihat=numpy.dot(P[u, :], Q[:, i])
                ujhat = numpy.dot(P[u, :], Q[:, j])
                # P[u,:]=P[u,:]-alpha*(sigmoid(ujhat-uihat)*(Q[:,j]-Q[:,i])+beta*P[u,:])
                # Q[:,j]=Q[:,j]-alpha*(P[u,:]*sigmoid(ujhat-uihat)+beta*Q[:,j])

                P[u, :] = P[u,:] - alpha * (
                    (1 - theta) * sigmoid(ujhat-uihat)*(Q[:,j]-Q[:,i]) - beta * P[u,:] +
                    theta * sigmoid(ej - cap[j]) * userp[i] * Q[:,j] *
                    sigmoid(ujhat) * sigmoid(-ujhat)
                )
                Q[:,i]=Q[:,i]-alpha*(-P[u,:]*sigmoid(ujhat-uihat)+beta*Q[:,i])

                Q[:, j] = Q[:,j] - alpha * (
                        (1 - theta) * P[u,:]*sigmoid(ujhat-uihat) - beta * Q[:,j] +
                        theta * sigmoid(ej - cap[j]) * userp[i] * P[u,:] *
                        sigmoid(ujhat) * sigmoid(-ujhat)
                )

                # P[i][k] = P[i][k] + alpha * (
                #         (1 - theta) * eij * Q[k][j] - beta * P[i][k] -
                #         theta * sigmoid(ej - cap[j]) * userp[i] * Q[k][j] *
                #         sigmoid(eijhat) * sigmoid(-eijhat)
                # )
                # Q[k][j] = Q[k][j] + alpha * (
                #         (1 - theta) * eij * P[i][k] - beta * Q[k][j] -
                #         theta * sigmoid(ej - cap[j]) * userp[i] * P[i][k] *
                #         sigmoid(eijhat) * sigmoid(-eijhat)
                # )





        orderloss=0
        for (u,i,j) in order:
            uihat=numpy.dot(P[u, :], Q[:, i])
            ujhat = numpy.dot(P[u, :], Q[:, j])
            orderloss+=sigmoid(uihat-ujhat)

        regloss=numpy.linalg.norm(P)+numpy.linalg.norm(Q)
        logging.debug("Total loss is %2.f %.2f  after %d iterations", orderloss,numpy.linalg.norm(Q), step + 1)
    return numpy.dot(P, Q)






def bmf(R, K=20, steps=25, alpha=0.01, beta=0.1):
    logging.info("Parameters for BMF: K=%d, steps=%d, alpha=%f, beta=%f", K, steps, alpha, beta)
    N = len(R)
    M = len(R[0])

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)
    BU = numpy.random.rand(N)
    BI = numpy.random.rand(M)
    Q = Q.T
    sum = 0
    count = 0
    for i in xrange(N):
        for j in xrange(M):
            if R[i][j] > 0:
                sum += R[i][j]
                count += 1
    mean = sum / count
    prevloss = 0
    for step in xrange(steps):
        for i in xrange(N):
            for j in xrange(M):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j]) - mean - BU[i] - BI[j]
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (eij * P[i][k] - beta * Q[k][j])
                    BU[i] = BU[i] + alpha * (eij - beta * BU[i])
                    BI[j] = BI[j] + alpha * (eij - beta * BI[j])
        loss = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    loss += pow((R[i][j] - numpy.asscalar(numpy.dot(P[i, :], Q[:, j])) -
                                 BU[i] - BI[j] - mean), 2)
                    pi = 0
                    qj = 0
                    for k in xrange(K):
                        pi += pow(P[i][k], 2)
                        qj += pow(Q[k][j], 2)
                    loss += beta * (pow(pi, 0.5) + pow(qj, 0.5) + pow(BU[i], 2) + pow(BI[j], 2))

        logging.debug("Total loss is %.2f  after %d iterations", loss, step + 1)
        if prevloss != 0 and prevloss - loss < 100:
            logging.info("Converge after %d iterations", step + 1)
            break
        prevloss = loss
    logging.info("Total loss is %.2f", prevloss)
    EstR = numpy.zeros((N, M))
    for i in xrange(N):
        for j in xrange(M):
            EstR[i][j] = numpy.dot(P[i, :], Q[:, j]) + BU[i] + BI[j] + mean

    return EstR


def cmf(R, cap, userp, K=20, steps=25, alpha=0.01, beta=0.1, theta=0.2,met="ori", slope=0):
    logging.info("Parameters for CMF: K=%d, steps=%d, alpha=%f, beta=%f, theta=%f, method=%s,slope=%.2f"
                 , K, steps, alpha, beta, theta,met,slope)
    N = len(R)
    M = len(R[0])

    P = numpy.random.rand(N, K)
    Q = numpy.random.rand(M, K)

    Q = Q.T
    prevloss = 0
    for step in xrange(steps):
        for j in xrange(M):
            ej = 0
            for i in xrange(N):
                if R[i][j] == 0:  # TODO
                    ej += userp[i] * sigmoid(numpy.dot(P[i, :], Q[:, j]))  # calculating E(usage(j))
            for i in xrange(N):
                if R[i][j] > 0:
                    eijhat = numpy.dot(P[i, :], Q[:, j])
                    eij = R[i][j] - eijhat
                    if met=="ori":
                        for k in xrange(K):
                            P[i][k] = P[i][k] + alpha * (
                                (1 - theta) * eij * Q[k][j] - beta * P[i][k] -
                                theta * sigmoid(ej - cap[j]) * userp[i] * Q[k][j] *
                                sigmoid(eijhat) * sigmoid(-eijhat)
                            )
                            Q[k][j] = Q[k][j] + alpha * (
                                (1-theta)* eij * P[i][k] - beta * Q[k][j]-
                                theta * sigmoid(ej - cap[j]) * userp[i] * P[i][k] *
                                sigmoid(eijhat) * sigmoid(-eijhat)
                            )
                    if met=="linear":
                        for k in xrange(K):
                            if ej > cap[j]:
                                P[i][k] = P[i][k] + alpha * (
                                        (1 - theta) * eij * Q[k][j] - beta * P[i][k] -
                                        theta * sigmoid(ej - cap[j]) * userp[i] * Q[k][j] *
                                        sigmoid(eijhat) * sigmoid(-eijhat)
                                )
                                Q[k][j] = Q[k][j] + alpha * (
                                        (1 - theta) * eij * P[i][k] - beta * Q[k][j] -
                                        theta * sigmoid(ej - cap[j]) * userp[i] * P[i][k] *
                                        sigmoid(eijhat) * sigmoid(-eijhat)
                                )
                            else:
                                P[i][k] = P[i][k] + alpha * (
                                        (1 - theta) * eij * Q[k][j] - beta * P[i][k] +
                                        theta * slope * userp[i] * Q[k][j] *
                                        sigmoid(eijhat) * sigmoid(-eijhat)
                                )
                                Q[k][j] = Q[k][j] + alpha * (
                                        (1 - theta) * eij * P[i][k] - beta * Q[k][j] +
                                        theta * slope * userp[i] * P[i][k] *
                                        sigmoid(eijhat) * sigmoid(-eijhat)
                                )

        caploss = 0
        ratloss = 0
        regloss = 0
        for j in xrange(M):
            for i in xrange(N):
                eijhat = numpy.dot(P[i, :], Q[:, j])

                if R[i][j] > 0:
                    ratloss += pow((R[i][j] - numpy.asscalar(numpy.dot(P[i, :], Q[:, j]))), 2)
                    pi = 0
                    qj = 0
                    for k in xrange(K):
                        pi += pow(P[i][k], 2)
                        qj += pow(Q[k][j], 2)
                    regloss += (pow(pi, 0.5) + pow(qj, 0.5))
                else:
                    #if met=="linear" and
                    caploss += (1.0) * math.log(1 + numpy.exp(userp[i] * sigmoid(eijhat) - cap[j]))

        loss = theta * caploss + (1 - theta) * ratloss + beta * regloss

        logging.debug("caploss,ratloss,regloss loss,is %f, %.2f, %.2f, %.2f after %d iterations",
                      caploss, ratloss, regloss, loss, step + 1)
        if prevloss != 0 and prevloss - loss < 1:
            logging.info("Converge after %d iterations", step + 1)
            break
        prevloss = loss
    logging.info("Total loss is %.2f", prevloss)
    return numpy.dot(P, Q)



def sigmoid(x):
    return (1 / (1 + numpy.exp(-x)))

###############################################################################

# if __name__ == "__main__":
#
#     R=read.ratmatrix
#
#     N = len(R)
#     M = len(R[0])
#     K = 2
#
#     P = numpy.random.rand(N,K)
#     Q = numpy.random.rand(M,K)
#
#     nP, nQ = matrix_factorization(R, P, Q, K)
#     rhat=numpy.dot(nP,nQ)
#     for item in read.test:
#
