import pickle
from sklearn.metrics import classification_report, confusion_matrix
def load_model(file_name):
    classifier_f=open(file_name,"rb")
    classifier=pickle.load(classifier_f)
    classifier_f.close()
    return classifier
def predictions(data):
    classifierNB=load_model('predictions(1).pickle')
    y_predict_test = classifierNB.predict(data)
    return y_predict_test