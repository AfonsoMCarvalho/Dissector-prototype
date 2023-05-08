import argparse
import re
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import pandas
import numpy as np

def main(train_file, test_file, output_file, output_md, no_scaling):
    # Detecting mode
    mode = None
    if re.search('joint',train_file) != None: mode = 'joint'
    elif re.search('fetch',train_file) != None: mode = 'fetch'
    elif re.search('reply',train_file) != None: mode = 'reply'
    else:
        print('ERROR DETECTING MODE. ABORTING')
        return

    # Ensuring test file is of the same mode
    if re.search(mode,test_file) == None:
        print('TEST FILE MODE MUST MATCH TRAIN FILE\'S. ABORTING')
        return

    # Get datasets
    train_set = pandas.read_csv(train_file)
    test_set = pandas.read_csv(test_file)

    # Dealing with infinite Differential Entropy values (replacing with max and min of the column)
    max = findMax(train_set['Differential_Entropy_'+mode])
    min = findMin(train_set['Differential_Entropy_'+mode])

    train_set['Differential_Entropy_'+mode].replace(np.inf, max, inplace=True)
    train_set['Differential_Entropy_'+mode].replace(-np.inf, min, inplace=True)

    max = findMax(test_set['Differential_Entropy_'+mode])
    min = findMin(test_set['Differential_Entropy_'+mode])

    test_set['Differential_Entropy_'+mode].replace(np.inf, max, inplace=True)
    test_set['Differential_Entropy_'+mode].replace(-np.inf, min, inplace=True)

    # Normalizing the data
    if no_scaling:
        std_train_set = train_set
        std_test_set = test_set
    else:    
        std_train_features = StandardScaler().fit_transform(train_set.values)
        std_train_set = pandas.DataFrame(std_train_features,train_set.index,train_set.columns)
        std_test_features = StandardScaler().fit_transform(test_set.values)
        std_test_set = pandas.DataFrame(std_test_features,test_set.index,test_set.columns)

    # Creating validation and training sets
    vals = []
    trains = []
    for i in [45, 71, 20, 84, 97, 17, 80, 10, 48, 32]:
        validation_set = std_train_set.sample(round(std_train_set.shape[0]/10),random_state=i)
        std_train_set = std_train_set.drop(validation_set.index)
        vals.append(validation_set)
        trains.append(std_train_set)

    # Perform Grid Search and collect results
    rbf_result_dic = {'kernel': [],
                      'gamma': [],
                      'tolerance': [],
                      'nu': [],
                      'validation_accuracy_%': [],
                      'test_accuracy_%': []}

    linear_result_dic = {'kernel': [],
                         'tolerance': [],
                         'nu': [],
                         'validation_accuracy_%': [],
                         'test_accuracy_%': []}

    poly_result_dic = {'kernel': [],
                       'degree': [],
                       'gamma': [],
                       'coef0': [],
                       'tolerance': [],
                       'nu': [],
                       'validation_accuracy_%': [],
                       'test_accuracy_%': []}

    sigmoid_result_dic = {'kernel': [],
                          'gamma': [],
                          'coef0': [],
                          'tolerance': [],
                          'nu': [],
                          'validation_accuracy_%': [],
                          'test_accuracy_%': []}
    ## Calculate iterations
    total1 = 0
    for gamma in ['scale','auto']:
        tolerance = 1e-1
        while tolerance >= 1e-10:
            for n in range(0,100,5):
                total1 += 1
            tolerance /= 10
    total = total1

    #______________________
    cache_size = 1000
    shrinking = True
    i=0
    for kernel in ['rbf','poly','sigmoid','linear']:
        if kernel == 'rbf':
            for gamma in ['scale','auto']:
                tolerance = 1e-1
                while tolerance > 1e-10:
                    for n in range(0,100,5):
                        nu = n / 100
                        i+=1
                        print(f'Progress: {i}/{total}',end='\r')
                        rbf_result_dic['kernel'].append(kernel)
                        rbf_result_dic['gamma'].append(gamma)
                        rbf_result_dic['tolerance'].append(tolerance)
                        rbf_result_dic['nu'].append(nu)
                        
                        val_accs = []
                        t_accs = []
                        for j in range(10):
                            try:
                                clf = svm.OneClassSVM(kernel = kernel, gamma = gamma, tol = tolerance, nu = nu, shrinking = shrinking, cache_size = cache_size).fit(trains[j])
                            except:
                                val_accs.append(-1)
                                t_accs.append(-1)
                                continue
                            
                            try:
                                val_pred = clf.predict(vals[j])
                                val_accs.append(round(len(val_pred[val_pred == 1])/len(val_pred)*100,2))
                                test_pred = clf.predict(std_test_set)
                                t_accs.append(round(len(test_pred[test_pred == -1])/len(test_pred)*100,2))

                            except:
                                val_accs.append(-1)
                                t_accs.append(-1)
                                continue

                        rbf_result_dic['validation_accuracy_%'].append(np.mean(val_accs) if -1 not in val_accs else -1)
                        rbf_result_dic['test_accuracy_%'].append(np.mean(t_accs) if -1 not in t_accs else -1)

                    tolerance /= 10
            print('\nRBF FINISHED')
        # if kernel == 'linear':
        #     tolerance = 1e-1
        #     while tolerance > 1e-10:
        #         for n in range(0,100,5):
        #             nu = n / 100
        #             i+=1
        #             print(f'Progress: {i}/{total}',end='\r')
        #             linear_result_dic['kernel'].append(kernel)
        #             linear_result_dic['tolerance'].append(tolerance)
        #             linear_result_dic['nu'].append(nu)
                    
        #             try:
        #                 clf = svm.OneClassSVM(kernel = kernel, tol = tolerance, nu = nu, shrinking = shrinking, cache_size = cache_size).fit(std_train_set)
        #                 val_pred = clf.predict(validation_set)
        #                 test_pred = clf.predict(std_test_set)

        #                 linear_result_dic['validation_accuracy_%'].append(round(len(val_pred[val_pred == 1])/len(val_pred)*100,2))
        #                 linear_result_dic['test_accuracy_%'].append(round(len(test_pred[test_pred == -1])/len(test_pred)*100,2))

        #             except:
        #                 linear_result_dic['validation_accuracy_%'].append(-1)
        #                 linear_result_dic['test_accuracy_%'].append(-1)
        #                 continue
        #         tolerance /= 10
        #     print('\nLINEAR FINISHED')
        # wlif kernel == 'poly':
        #     for degree in range(1,6,1):
        #         for gamma in ['scale','auto']:
        #             for coef0 in range(0,5,1):
        #                 tolerance = 1e-1
        #                 while tolerance > 1e-10:
        #                     for n in range(0,100,5):
        #                         nu = n / 100
        #                         i+=1
        #                         print(f'Progress: {i}/{total}',end='\r')
        #                         poly_result_dic['kernel'].append(kernel)
        #                         poly_result_dic['degree'].append(degree)
        #                         poly_result_dic['gamma'].append(gamma)
        #                         poly_result_dic['coef0'].append(coef0)
        #                         poly_result_dic['tolerance'].append(tolerance)
        #                         poly_result_dic['nu'].append(nu)
                                
        #                         try:
        #                             clf = svm.OneClassSVM(kernel = kernel, degree = degree, gamma = gamma, coef0 = coef0, tol = tolerance, nu = nu, shrinking = shrinking, cache_size = cache_size).fit(std_train_set)
        #                             val_pred = clf.predict(validation_set)
        #                             test_pred = clf.predict(std_test_set)

        #                             poly_result_dic['validation_accuracy_%'].append(round(len(val_pred[val_pred == 1])/len(val_pred)*100,2))
        #                             poly_result_dic['test_accuracy_%'].append(round(len(test_pred[test_pred == -1])/len(test_pred)*100,2))

        #                         except:
        #                             poly_result_dic['validation_accuracy_%'].append(-1)
        #                             poly_result_dic['test_accuracy_%'].append(-1)
        #                             continue
        #                     tolerance /= 10
        #     print('\nPOLY FINISHED')
        # if kernel == 'sigmoid':
        #     for gamma in ['scale','auto']:
        #         for coef0 in range(0,5,1):
        #             tolerance = 1e-1
        #             while tolerance >= 1e-10:
        #                 for n in range(0,100,5):
        #                     nu = n / 100
                            
        #                     sigmoid_result_dic['kernel'].append(kernel)
        #                     sigmoid_result_dic['gamma'].append(gamma)
        #                     sigmoid_result_dic['coef0'].append(coef0)
        #                     sigmoid_result_dic['tolerance'].append(tolerance)
        #                     sigmoid_result_dic['nu'].append(nu)
                            
        #                     val_accs = []
        #                     t_accs = []
        #                     for j in range(10):
        #                         i+=1
        #                         print(f'Progress: {i}/{total}',end='\r')
        #                         try:
        #                             clf = svm.OneClassSVM(kernel = kernel, gamma = gamma, tol = tolerance, nu = nu, shrinking = shrinking, cache_size = cache_size).fit(trains[j])
        #                         except:
        #                             val_accs.append(-1)
        #                             t_accs.append(-1)
        #                             continue
                                
        #                         try:
        #                             val_pred = clf.predict(vals[j])
        #                             val_accs.append(round(len(val_pred[val_pred == 1])/len(val_pred)*100,2))
        #                             test_pred = clf.predict(std_test_set)
        #                             t_accs.append(round(len(test_pred[test_pred == -1])/len(test_pred)*100,2))

        #                         except:
        #                             val_accs.append(-1)
        #                             t_accs.append(-1)
        #                             continue

        #                     sigmoid_result_dic['validation_accuracy_%'].append(np.mean(val_accs) if -1 not in val_accs else -1)
        #                     sigmoid_result_dic['test_accuracy_%'].append(np.mean(t_accs) if -1 not in t_accs else -1)
        #                 tolerance /= 10
        #     print('\nSIGMOID FINISHED')
    
    results = [rbf_result_dic] #[rbf_result_dic, poly_result_dic, sigmoid_result_dic, linear_result_dic]

    # Build Dataframes with the results
    for dic in results:
        scaling = "no_scaling" if no_scaling else "scaling"
        out_csv = output_file.split('.')[0]+'_'+scaling+'_'+dic['kernel'][0]+'.'+output_file.split('.')[-1]
        df = pandas.DataFrame(dic)
        df.sort_values(by=['validation_accuracy_%','test_accuracy_%'], inplace=True, ascending=False)
        
        with open(out_csv,'w') as of:
            df.to_csv(of,index=False)
            of.close()

        with open(output_md,'a') as of:
            of.write(f'# {out_csv.split(".")[0].split("/")[-1]}:\n')    
            of.write(df.to_markdown())
            of.write('\n')
            of.close()

    return

def findMax(vector):
    max = None
    for value in vector:
        if value == np.inf or value == -np.inf: continue
        else:
            if max == None or value > max:
                max = value
    return max

def findMin(vector):
    min = None
    for value in vector:
        if value == np.inf or value == -np.inf: continue
        else:
            if min == None or value < min:
                min = value
    return min

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_file', type=str, default=None, help='The .csv file containing the training dataset (default: %(default)s)')
    parser.add_argument('test_file', type=str, default=None, help='The .csv file containing the dataset to classify (default: %(default)s)')
    parser.add_argument('output_file', type=str, default=None, help='The file where the output will be written as .csv (default: %(default)s)')
    parser.add_argument('output_md', type=str, default=None, help='The file where the output will be written in markdown tables (default: %(default)s)')
    parser.add_argument('-ns', action='store_true', help='Turn off data scaling (default: %(default)s)')
    
    args = parser.parse_args()
    train_file = args.train_file
    test_file = args.test_file
    output_file = args.output_file
    output_md = args.output_md
    no_scaling = args.ns

    main(train_file, test_file, output_file, output_md, no_scaling)