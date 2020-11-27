import pandas as pd
from fastDamerauLevenshtein import damerauLevenshtein
import numpy as np
#from tqdm import tqdm


class Prediction():
    Item = None
    Parent = None
    Children = None

    def __init__(self, itemValue=None):
        self.Item = itemValue
        self.Children = []
        self.Parent = None

    def get_child(self, target):
        for chld in self.Children:
            if chld.Item == target:
                return chld
        return None

    def get_children(self):
        return self.Children

    def has_child(self, target):
        found = self.get_child(target)
        if found is not None:
            return True
        else:
            return False

    def add_new_child(self, child):
        newchild = Prediction(child)
        newchild.Parent = self
        self.Children.append(newchild)

    def remove_child(self, child):
        for chld in self.Children:
            if chld.Item == child:
                self.Children.remove(chld)


class CPT():
    alphabet = None # create set of all unique items
    root = None     # root note of prediction tree
    II = None       # inverted index dictionary with key: unique item, value: set of sentences containing the item
    LT = None       # lookup table dictionary with key: id of a sequence (row), value: leaf node of prediction tree
    def __init__(self):
        self.alphabet = set()
        self.root = Prediction()
        self.II = {}
        self.LT = {}

    def load_files(self, train_file, test_file=None):
        """
        This function reads in the wide csv file of sequences separated by commas and returns a list of list of those
        sequences. The sequences are defined as below.
        seq1 = A,B,C,D
        seq2  B,C,E
        Returns: [[A,B,C,D],[B,C,E]]
        """

        data = [] # list of lists containing sequence data for training
        target = [] # list of lists containing test sequences to be predicted

        if train_file is None:
            return train_file

        train = pd.read_csv(train_file, header=0)

        for index, row in train.iterrows():
            data.append(row.values)

        if test_file is not None:

            test = pd.read_csv(test_file, header=None)

            for index, row in test.iterrows():
                data.append(row.values)
                target.append(list(row.values))

            return data, target


    def train(self, data):
        """
         This functions populates the Prediction Tree, Inverted Index and LookUp Table for the algorithm.
         Input: The list of list training data
         Output : Boolean True
         """

        cursornode = self.root

        for seqid, row in enumerate(data):
            for element in row:
                # adding to prediction tree
                if element==element: # different sequence length support
                    if cursornode.has_child(element) == False:
                        cursornode.add_new_child(element)
                        cursornode = cursornode.get_child(element)

                    else:
                        cursornode = cursornode.get_child(element)

                # adding to the inverted index

                    if self.II.get(element) is None:
                        self.II[element] = set()

                    self.II[element].add(seqid)

                    self.alphabet.add(element)

            self.LT[seqid] = cursornode

            cursornode = self.root

        return True

    def score(self, counttable, key, length, target_size, number_of_similar_sequences, number_items_counttable):
        """
         This functions populates the Prediction Tree, Inverted Index and LookUp Table for the algorithm.
         Input: The list of list training data
         Output : Boolean True
         """

        weight_level = 1 / number_of_similar_sequences
        weight_distance = 1 / number_items_counttable
        score = 1 + weight_level + weight_distance * 0.001

        if counttable.get(key) is None:
            counttable[key] = score
        else:
            counttable[key] = score * counttable.get(key)

        return counttable

    def predict(self, data, target, k, n=1):
        """
        Here target is the test dataset in the form of list of list,
        k is the number of last elements that will be used to find similar sequences and,
        n is the number of predictions required.
        Input: training list of list, target list of list, k,n
        Output: max n predictions for each sequence
        """

        predictions = []

        #for each_target in tqdm(target):
        for each_target in target:
            # different sequence length support
            i = 0
            while i < len(each_target) and each_target[i] == each_target[i]:  # find NaN start
                i = i + 1
            l = i - k - 1
            if l < 0:
                l = 0

            each_target = each_target[l:i]

            intersection = set(range(0, len(data)))

            for element in each_target:
                if self.II.get(element) is None:
                    continue
                intersection = intersection & self.II.get(element)

            similar_sequences = []

            for element in intersection:
                currentnode = self.LT.get(element)
                tmp = []
                while currentnode.Item is not None:
                    tmp.append(currentnode.Item)
                    currentnode = currentnode.Parent
                similar_sequences.append(tmp)

            for sequence in similar_sequences:
                sequence.reverse()

            counttable = {}

            for sequence in similar_sequences:
                try:
                    index = next(
                        i for i, v in zip(range(len(sequence) - 1, 0, -1), reversed(sequence)) if v == each_target[-1])
                except:
                    index = None
                if index is not None:
                    count = 1
                    for element in sequence[index + 1:]:
                        if element in each_target:
                            continue

                        counttable = self.score(counttable, element, len(each_target), len(each_target),
                                                len(similar_sequences), count)
                        count += 1

            pred = self.get_n_largest(counttable, n)
            predictions.append(pred)

        return predictions

    def get_n_largest(self, dictionary, n):

        largest = sorted(dictionary.items(), key=lambda t: t[1], reverse=True)[:n]
        return [key for key, _ in largest]


model = CPT()

data, target = model.load_files('data/h03_train.csv', 'data/h03_test.csv')

model.train(data)

predictions = model.predict(data, target, 3, 5)

# for sequence in data:
#     prediction = model.predict(data,target,k=3,n=len(sequence))
#     print('For sequence {0} prediction is {1}'.format(sequence, prediction))


i = 0
distances = []
print()
for elem in predictions:
    pred = [x for x in target[i] if str(x) != 'nan']
    dat = [x for x in data[i] if str(x) != 'nan']
    predicted = str(''.join(pred) + ''.join(elem))
    observed = ''.join(dat)
    dl = damerauLevenshtein(predicted, observed)
    distances.append(dl)
    print(target[i])
    print('for sequence {0} prediction is {1}'.format(i, elem))
    print('edit distance between {0} and {1}: {2}'.format(predicted, observed, dl))
    i += 1
    print('----------')

print('Average similarity: {0}'.format(np.mean(distances)))
