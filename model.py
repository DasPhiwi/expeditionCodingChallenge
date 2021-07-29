import pickle
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import  numpy as np
_training_data = pd.read_csv("data.csv")
_training_label = pd.read_csv("labels.csv")
def _train_model(training_data,training_label, save_file = "model.sav"):
    clf =  MLPRegressor(random_state=1, max_iter=500).fit(training_data,training_label)
    filename = 'finalized_model.sav'
    pickle.dump(clf, open(save_file, 'wb'))
def _evaluate_model(X_test, y_test, model_file = "model.sav"):
    clf = pickle.load(open(model_file, 'rb'))
    score = clf.score(X_test, y_test)
    #print(score)
    return score
def prediction_(data, model_file = "model.sav"):
    clf = pickle.load(open(model_file, 'rb'))
    result = clf.predict(data)
    #print(result)
    return result
#_train_model(_training_data[['lightOn', 'windowsOpen', 'rollerBlindsClosed', 'airConditioningRunning',
                                    #       'heaterRunning']].values, _training_label["powerConsumption"].values)
#prediction_(_training_data[['lightOn', 'windowsOpen', 'rollerBlindsClosed', 'airConditioningRunning',
#                                           'heaterRunning']].values, model_file = "model.sav")
