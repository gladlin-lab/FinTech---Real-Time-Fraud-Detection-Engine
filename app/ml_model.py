import pickle

model = pickle.load(open("model.pkl","rb"))

def ml_score(amount):
    return abs(model.decision_function([[amount]])[0])
