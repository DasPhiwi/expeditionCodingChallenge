import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import  numpy as np
#_training_data = pd.read_csv("data.csv")
#_training_label = pd.read_csv("labels.csv")
def _train_model(training_data,training_label, save_file = "model.npy"):
    X_train, X_test, y_train, y_test = train_test_split(training_data, training_label, stratify=training_label,
                                                        random_state=1)
    clf = MLPRegressor(random_state=1, max_iter=500, verbose=True).fit(X_train, y_train)
    np.save(save_file, clf)
def _evaluate_model(X_test, y_test, model_file = "model.npy"):
    clf = np.load(model_file)
    score = clf.score(X_test, y_test)
    print(score)
    return score
def prediction_(data, model_file = "model.npy"):
    clf = np.load(model_file)
    result = clf.predict(data)
    return result