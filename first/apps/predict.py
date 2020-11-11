import pickle
from sklearn.metrics import classification_report, confusion_matrix
def load_model(file_name):
    classifier_f=open(file_name,"rb")
    classifier=pickle.load(classifier_f)
    classifier_f.close()
    return classifier
def predictions(data):
    with open('apps/predictions.pickle','rb') as f:
        classifierNB=pickle.load(f)
    return classifierNB.predict(data)