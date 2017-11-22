# HMM_POS

# Disclaimer for future 10-601 students at CMU: This code is part of an assignment submitted to CMU, and all future submissions by students will be testing against it for cheating.


The Viterbi algorithm is a dynamic programming algorithm that computes the most likely state transition path given an observed sequence of symbols. It is very similar to the forward algorithm, except that we will be taking a max(·), rather than a P(·), over all possible ways to arrive at the current state.

The Viterbi algorithm is implemented to extract the most likely state sequence in viterbi.py. The command-line signature of this script should be as follows:
$ python viterbi.py <dev> <hmm-trans> <hmm-emit> <hmm-prior>
Here, the four arguments should be in the format of dev.txt, hmm-trans.txt, hmm-emit.txt and hmm-prior.txt respectively. This implementation treats each sentence as a separate observed sequence and compute its Viterbi path separately.

The contents and formatting of each of the input files is explained below.
# hmm-trans.txt, hmm-emit.txt and hmm-prior.txt

These files contain pre-trained model parameters of an HMM that you can use for testing your implementation of the Evaluation and Decoding problems. The format of the first two files are analogous and is as follows: 

Every line in these files consists of a conditional probability distribution. In the case of transition probabilities, this distribution corresponds to the probability of transitioning into another state, given a current state. Similarly, in the case of emission probabilities, this distribution corresponds to the probability of emitting a particular symbol,
given a current state. 
For example, every line in hmm-trans.txt has the following format: <Curr-State> <Nxt-State0>:<Prob-Val0> ... <Nxt-StateN>:<Prob-ValN>. The format of hmm-prior.txt is slightly different and only contains a single probability distribution over starting states. Each line contains the name of a state and its associated starting probability value, like so: <State0> <Prob-Val0>.

# dev.txt
This file contains plain text data that you can use in testing your implementation of the Decoding problems. Specifically the text contains one sentence per line that has already been pre-processed, cleaned and tokenized. You do not need to perform any processing of any kind. You should treat every line as a separate sequence and assume that it has the following format:
<Word0> <Word1> ... <WordN>
where every <WordK> unit token is whitespace separated. Note that dev.txt is the plain text version of dev-tag.txt.

