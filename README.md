# CS-variability-adaptation

This code will explore various effects of noise on the compressed-sensing framework in odor sensing. The applicability of compressed sensing to olfaction has been investigated in some recent papers: see [Krishnamurthy et al](https://arxiv.org/abs/1707.01962) and [Zhang et al](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004850). 

Compressed sensing passes a sparse high-dimensional signal $\mathbf s^0$ through a measurement matrix $\mathbf R$ that projects the signal to a lower-dimensional space to produce a measured signal $\mathbf x$ . Despite this disparity in measurement and signal dimension, the signal can be encoded with high fidelity, assuming a sufficient level of sparsity. 

The code investigates the following:

1. The effect of nonzero perturbations on the nonzero components of the sparse odor signal. 
2. The effect of a slow, dynamical nonlinearity $f$ , between the signal and linear response, $\mathbf s^0 \rightarrow f \rightarrow \mathbf R$, that can adapt to changing backgrounds to retain signal sensitivity.

In particular, how do these modifications affect the information transfer? 

