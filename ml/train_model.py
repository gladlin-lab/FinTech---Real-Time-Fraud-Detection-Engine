from sklearn.ensemble import IsolationForest
import pickle

data = [[100],[200],[500],[1000],[5000],[10000]]
model = IsolationForest()
model.fit(data)

pickle.dump(model, open("model.pkl","wb"))
print("Model trained")
