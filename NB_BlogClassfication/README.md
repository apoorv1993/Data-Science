
# fdfdgdfgd
In this project a Naive Bayes classifier is implemented to classify a political blog as being “liberal” or “conservative”. The data set to be used for this project is a set of self-identified liberal and conservative blogs. The data is rearranged and preprocessed slightly. Each blog is stored in a separate file, within which each line is a separate word. The files split.train and split.test contain lists of files/blogs to be used for training and testing a classifier.

Usage: python nb.py split.train split.test

This program, named as nb.py will take a set of labeled training examples in split.train and a set of test examples split.test, and classify them using a Naive Bayes classifier. It assumes that all data files are in the same directory as this program. This program outputs the predicted labels for the test data, one per line, in the order they are listed in split.test, and calculate the accuracy on the test dataset. For simplicity purpose, it ignores case—treat “President” and “president” as the same word type.

It is general practice to preprocess datasets and remove stop words like “the”, “a”, “of”, etc. before training
a classifier. Rather than prespecifying a list of stop words, we can simply exclude the N most frequent words. Another classifier nbStopWords.py based on nb.py which additionally takes a parameter N and excludes the N most frequent words from its vocabulary before training the classifier. Here is the syntax for N = 10; the output will look like the output from
nb.py:

Usage: python nbStopWords.py split.train split.test 10

For smoothing in Naive Bayes classifier, we use a parameter q as specified in below formula:

                P(wk | v j) = (nk + q) /(n + q ·|Vocabulary|)
