from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC
# import libloader
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

data_frame = pd.read_csv("dataset.csv",header = 0,sep=',',on_bad_lines = 'skip')
data_frame = data_frame.iloc[:,1:11]
# extract features
x_features = data_frame.iloc[:,:-1].values
y_potability = data_frame.iloc[:,-1].values
# extract test train 
imputer = SimpleImputer(strategy='mean')
x_features = imputer.fit_transform(x_features)
x_train , x_test , y_train , y_test = train_test_split(x_features,y_potability,test_size=0.05,random_state=33)
# scale up dat
scaler0 = StandardScaler().fit(x_train)
x_train = scaler0.transform(x_train)
x_test = scaler0.transform(x_test)
scaler1 = RobustScaler().fit(x_train)
x_train = scaler1.transform(x_train)
x_test = scaler1.transform(x_test)
# creting model
base_cls = SVC(kernel='rbf', random_state = 21,gamma='auto',C=1.5)
cls = CalibratedClassifierCV(base_cls,cv=2,method='isotonic')
cls.fit(x_train, y_train)
y_pred = cls.predict(x_test)

print("Train accuracy : " + str(accuracy_score(y_train,cls.predict(x_train))))
print("Test accuracy : " + str(accuracy_score(y_test,cls.predict(x_test))))

rng = np.random.default_rng()
def predict(ph,tds):
    random_indices = np.random.choice(1000,  size=1,  replace=False) 
    features = data_frame[data_frame['Potability'] == 1].iloc[random_indices, :-1].values
    features = imputer.transform(features)
    features[:,0] = ph
    features[:,2] = tds
    # if tds >= 500 or tds <= 10:
    #     return [0,0]
    # if ph < 5.5 or ph > 8.5:
    #     return [0,0]
    # print(features)
    features = scaler0.transform(features)
    features = scaler1.transform(features)
    pred = cls.predict_proba(features)
    return pred[0]

# print(predict(7.0,150))