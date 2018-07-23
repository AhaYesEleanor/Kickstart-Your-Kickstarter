
# coding: utf-8

# In[ ]:


from pprint import pprint

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn import model_selection


# In[ ]:


def perform_grid_search(train_X,train_y,val_X,val_y, 
                        params_to_check={'penalty': ['l1','l2'], 
                                         'C': [50, 100, 500, 1000], 
                                         'class_weight': [None, 'balanced']},):
    #reg_parameter_values = [0.05-.95, 1, 10, 25, 50, 100]
    #parameters = {'penalty': ['l1','l2'], 'C': reg_parameter_values, 'class_weight': [None, 'balanced']}
    grid = model_selection.GridSearchCV(LogisticRegression(),param_grid=params_to_check, cv=5, scoring='roc_auc', n_jobs=1)
    grid_search = grid.fit(train_X, train_y)
    print('best params ', grid_search.best_params_)
    print('best train AUC score: ', grid_search.best_score_)
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(val_X)
    
    conf_mat = confusion_matrix(val_y, y_pred)
    print('best confusion matrix: ')
    print(conf_mat)
    
    print('validation AUC score: ', roc_auc_score(val_y, y_pred))
    print('best_model_coefs:')
    pprint(list(zip(train_X.columns, best_model.coef_[0])))
    return best_model, roc_auc_score(val_y, y_pred)

