import numpy as np
import pandas as pd
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import matplotlib.pyplot as plt

#dataset de doenças cardíacas
df = pd.read_csv('heart.csv')

X = df['Cholesterol']
y = df['HeartDisease']
#dividindo em etapas de treino
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)
print(f"Training target statistics: {Counter(y_train)}")
print(f"Testing target statistics: {Counter(y_test)}")

#algoritmo SMOTE de oversampling
sm = SMOTE(random_state=42)
X_train = X_train.values.reshape(-1, 1)
y_train = y_train.values.reshape(-1, 1)
X_res, y_res = sm.fit_resample(X_train, y_train)
print(f"Training target statistics: {Counter(y_res)}")
print(f"Testing target statistics: {Counter(y_test)}")

#matriz de confusão
svc = SVC(kernel='linear', C=10.0, random_state=1)
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test.values.reshape(-1, 1))
conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
fig, ax = plt.subplots(figsize=(5, 5))
ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
 
plt.xlabel('Predictions', fontsize=18)
plt.ylabel('Actuals', fontsize=18)
plt.title('Confusion Matrix', fontsize=18)
plt.show()
#precisão, verdadeiros positivos / ( falso positivos + verdadeiros positivos)
print('Precision: %.3f' % precision_score(y_test, y_pred))
#recall, verdadeiros positivos / ( falso negativos + verdadeiros positivos)
print('Recall: %.3f' % recall_score(y_test, y_pred))
#acurácia, (verdadeiros positivos + verdadeiros negativos) / (verdadeiros positivos + falso negativos + verdadeiros negativos + falso positivos)
print('Accuracy: %.3f' % accuracy_score(y_test, y_pred))
#score f1 = 2*precisão *recall / (precisão + recall)
print('F1 Score: %.3f' % f1_score(y_test, y_pred))

#remoção de outliers com colesterol irreal
df1 = df[df['Cholesterol']>=80]
#algoritmo estatístico para remoção de outliers baseado em ser a média +- 2 desvios padrões
def removeoutliers(df, x):
  mean = np.mean(df[x], axis=0)
  sd = np.std(df[x], axis=0)
  df = df[df[x]> mean - 2 * sd]
  df = df[df[x]< mean + 2 * sd]
  return df
prenormalized = [df1['Cholesterol']]
normalized = preprocessing.normalize(prenormalized)
print("Normalized Data = ", normalized)
df_filtrado = removeoutliers(df1,'RestingBP')
print(df_filtrado)
#nao tem duplicados, duplicando dataframe e depois removendo duplicados
dfduplicado = pd.concat([df_filtrado,df_filtrado])
print(dfduplicado)
dfduplicado = dfduplicado.drop_duplicates(keep='last')
print(dfduplicado)
#nao tem dados ausentes, usando outro dataset
data = {'set_of_numbers': [1,2,3,4,5,np.nan,6,7,np.nan,np.nan,8,9,10,np.nan]}
dfausente = pd.DataFrame(data)
print(dfausente)
dfausente = dfausente.fillna(0)
print(dfausente)
