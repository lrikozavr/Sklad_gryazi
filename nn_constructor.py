# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
    
import time
def loading_progress_bar(percent):
    bar_length = 50
    filled_length = int(percent/100 * bar_length)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {percent:.0f}% ', end='')

import math
def ActivationFunction(name,value):
       
    # функція активації
    def sigmoid(x):
      return 1/(1+math.exp(-x))
    
    def relu(x):
        if(x < 0):
            return 0
        return x
    
    def linear(x):
      return x
    # деривативна функція активації
    def derivative_sigmoid(x):
      return sigmoid(x) * (1 - sigmoid(x))
    
    def derivative_relu(x):
        if(x < 0):
           return 0
        return 1
    
    def derivative_linear(x):
      return 1
    
    match name:
        case 'linear':
            return linear(value)
        case 'relu':
            return relu(value)
        case 'sigmoid':
            return sigmoid(value)
        case 'derivative_linear':
            return derivative_linear(value)
        case 'derivative_relu':
            return derivative_relu(value)
        case 'derivative_sigmoid':
            return derivative_sigmoid(value)
        case _:
            Exception('Wrong activationfunction name')

def LossFunction(name,y_prob,y):
    # квадратична функція втрат
    def square(y_prob,y):
        return 0.5*pow(y_prob-y,2)
    # деривативна версія
    def derivative_square(y_prob,y):
        return y_prob-y
    
    match name:
       case 'square':
          return square(y_prob,y)
       case 'derivative_square':
          return derivative_square(y_prob,y)
       case _:
          Exception('Wrong lossfunction name')
#print(activation_function('sigmoid',10.0))
#print(activation_function('linear',10.0))

class Optimizer():
    time_step_epoch = 1
    e = 1e-4
    alpha = 0.5

    def __init__(self):
        pass
    
    def __init__(self,log):
        self.mv = []
        #self.mv.append([])
        #1=0
        for index in range(1,len(log),1):
            self.mv.append(np.zeros((2,log[index][1],log[index-1][1])))
        #self.mv = np.array(self.mv)

    def adam(self,layer_index,i,j,grad_value,b1 = 0.9,b2 = 0.99):
        self.mv[layer_index-1][0][i][j] = b1*self.mv[layer_index-1][0][i][j] + (1-b1)*grad_value
        self.mv[layer_index-1][1][i][j] = b2*self.mv[layer_index-1][1][i][j] + (1-b2)*grad_value**2
        mt = self.mv[layer_index-1][0][i][j]/(1-pow(b1,self.time_step_epoch))
        vt = self.mv[layer_index-1][1][i][j]/(1-pow(b2,self.time_step_epoch))
        return -self.alpha*mt/(pow(vt,0.5) + self.e)

    def grad(self,grad_value):
        return -self.alpha*grad_value

    def optimizer(self,name,grad_value,layer_index,i,j):
        match name:
          case 'adam':
              return self.adam(layer_index,i,j,grad_value)
          case 'grad':
              return self.grad(grad_value)

class Dense():
    neuron_count = 1
    
    def __init__(self):
        pass
    
    def __init__(self,neuron_count, activation_function = 'linear', first_layer = 'yes'):
        if(not first_layer == 'yes'):
            self.neuron_weight = np.ones((2,neuron_count,first_layer.neuron_count))
            self.neuron_value = np.zeros((2,neuron_count))
        else:
            self.neuron_weight = np.ones((1,neuron_count)) 
            self.neuron_value = np.zeros((1,neuron_count))
        self.activation_function = activation_function
        self.first_layer = first_layer
        self.neuron_count = neuron_count

class Model():

    #optimizer = Optimizer()
    optimiser_name = 'grad'

    def __init__(self):
        pass
    
    def get_neuron_network_from_dense_class(self,a):
        network = []
        neuron_count = a.neuron_count
        if (a.first_layer == 'yes'):
            network.append(np.array([(a.activation_function,a.neuron_value,a.neuron_weight)],
                                    np.dtype([('activation_function',object),
                                    ('neuron_value','f8',(1,neuron_count)),
                                    ('neuron_weight','f8',(1,neuron_count))])))
            return network

        network = self.get_neuron_network_from_dense_class(a.first_layer)

        last_neuron_count = a.first_layer.neuron_count
        network.append(np.array([(a.activation_function,a.neuron_value,a.neuron_weight)],
                                np.dtype([('activation_function',object),
                                ('neuron_value','f8',(2,neuron_count)),
                                ('neuron_weight_value','f8',(2,neuron_count,last_neuron_count))])))
        
        return network

    def return_network_log(self,a):
        log = []
        if (a.first_layer == 'yes'):
            log.append([a.activation_function,a.neuron_count])
            return log
        log = self.return_network_log(a.first_layer)
        log.append([a.activation_function,a.neuron_count])
        return log
    
    def return_network_from_log(self,log):
        network = []    
        network.append(np.array([(log[0][0],np.zeros((1,log[0][1])),np.zeros((1,log[0][1])))],
                                np.dtype([('activation_function',object),
                                ('neuron_value','f8',(1,log[0][1])),
                                ('neuron_weight','f8',(1,log[0][1]))])))
        for layer_index in range(1,self.layer_count,1):
            network.append(np.array([(log[layer_index][0],np.zeros((2,log[layer_index][1])),np.ones((2,log[layer_index][1],log[layer_index-1][1])))],
                                np.dtype([('activation_function',object),
                                ('neuron_value','f8',(2,log[layer_index][1])),
                                ('neuron_weight_value','f8',(2,log[layer_index][1],log[layer_index-1][1]))])))
        return network

    def __init__(self,dense_class_item):
        self.neural_network = self.get_neuron_network_from_dense_class(dense_class_item)
        self.neural_network_log = self.return_network_log(dense_class_item)
        #print(self.neural_network_log)
        #print(self.neural_network)
        self.layer_count = len(self.neural_network_log)
        #print(self.layer_count)
        #self.neural_network = self.return_network_from_log(self.neural_network_log)
        #print(self.neural_network_log)
        self.optim = Optimizer(self.neural_network_log)
        

    def perseptron(self,neural_network_value,layer_index,neuron_index):
      if(layer_index > 0 and layer_index < self.layer_count):
        if(neuron_index >= 0 and neuron_index < self.neural_network_log[layer_index][1]):
          sum = neural_network_value[layer_index][0][2][0][neuron_index,:].dot(neural_network_value[layer_index-1][0][1][0,:]) + np.random.random()/1000.0
            #
          neural_network_value[layer_index][0][1][0][neuron_index] = ActivationFunction(neural_network_value[layer_index][0][0],sum)
          neural_network_value[layer_index][0][1][1][neuron_index] = ActivationFunction(f"derivative_{neural_network_value[layer_index][0][0]}",sum)

    def per_all_at_once(self,neural_network_value):
      for layer_index in range(1,self.layer_count,1):
        for j in range(self.neural_network_log[layer_index][1]):
          self.perseptron(neural_network_value,layer_index,j)

    def perceptron_grad(self,nn_value,layer_index,i,j):
        if(layer_index > 0):
            if(layer_index < self.layer_count-1):
                nn_value[layer_index][0][2][1][i][j] = (nn_value[layer_index-1][0][1][0][j]/(nn_value[layer_index][0][1][0][j] ))*nn_value[layer_index][0][1][1][i]*nn_value[layer_index+1][0][2][0][:,i].dot(nn_value[layer_index+1][0][2][1][:,j])
            elif(layer_index == self.layer_count-1):
                nn_value[layer_index][0][2][1][i][j] = nn_value[layer_index][0][1][1][i]*nn_value[layer_index-1][0][1][0][j]
    
    def grad_all_at_once(self,nn_value):
        for layer_index in range(self.layer_count-1,0,-1):
            for i in range(self.neural_network_log[layer_index][1]):
                for j in range(self.neural_network_log[layer_index-1][1]):
                    self.perceptron_grad(nn_value,layer_index,i,j)

    def backpropagation(self,nn_value,opti,y):
        self.grad_all_at_once(nn_value)

        for layer_index in range(self.layer_count - 1,0,-1):
            #print(layer_index)
            for i in range(self.neural_network_log[layer_index][1]):
                for j in range(self.neural_network_log[layer_index - 1][1]):
                    nn_value[layer_index][0][2][0][i][j] +=  LossFunction(name = 'derivative_square',
                                                                       y_prob = nn_value[self.layer_count-1][0][1][0][0],
                                                                       y = y)*opti.optimizer(name = self.optimiser_name,
                                                                                                grad_value = nn_value[layer_index][0][2][1][i][j],
                                                                                                layer_index=layer_index,i=i,j=j)
                    
       
    '''
    def fit_NN_one(self,nn_value,opti,x,y,epochs):
        #print(self.network_neuron_value)
        
        #opti = Optimizer(self.neural_network_log)
        #self.optimizer_name = 'adam'
        nn_value[0][1][0,:] = x
        opti.time_step_epoch = 1
        for epoch in range(epochs):
            opti.time_step_epoch += epoch
            self.per_all_at_once(nn_value)
            self.backpropagation(nn_value,opti,y)
        self.per_all_at_once(nn_value)
        return LossFunction('square',nn_value[self.layer_count-1][1][0][0],y)
    '''
    def fit_one_nn(self,nn_value,opti,x,y,epoch):
        nn_value[0][0][1][0,:] = x
        # треба прослідкувати щоб воно не давало посилання на self змінну, а передавало його значення
        # бо інакше воно буде працювати некоректно
        
        #nn_value = self.neural_network
        #opti.mv = self.optim.mv
        #print(nn_value[1])
        for layer_index in range(1,self.layer_count,1):
            nn_value[layer_index][0][2] = self.neural_network[layer_index][0][2]
            opti.mv[layer_index-1] = self.optim.mv[layer_index-1]
        
        #self.neural_network[1][0][2][0][1][1] = 23
        #print(nn_value[1])
        #print(self.neural_network[1])
        #exit()
        #print(nn_value[3])
        #exit()
        #
        opti.time_step_epoch = epoch
        #print(nn_value)
        self.per_all_at_once(nn_value)
        #print(nn_value)
        #print(nn_value[2][0][2])
        self.backpropagation(nn_value,opti,y)
        #print(nn_value[2][0][2])
        
        #print()
        self.per_all_at_once(nn_value)
        #exit()
        #nn_sum[1:(self.layer_count-1),2] += nn_value[1:(self.layer_count-1),2]
        #opti_sum += opti.mv
        return LossFunction('square',nn_value[self.layer_count-1][0][1][0][0],y)

    def fill_weight(self,mass,value,name):
        match name:
            case 'w':
                for layer_index in range(self.layer_count):
                    mass[layer_index][0][2].fill(value)
            case 'm':
                for layer_index in range(self.layer_count-1):
                    mass[layer_index][0].fill(value)
            case _:
              Exception('')
           

    
    def batch_separate(self,x,y,nn_sum,optim_sum,batch_size_nn,batch_size_optim,count_label,batch_size,epoch = 1,thread = 16):
        batch_count = count_label // batch_size
        #print(batch_count)
        for index_batch in range(0, batch_count, 1):
            loading_progress_bar(index_batch / batch_count * 100)
            import time
            #time.sleep(0.001)
            #
            #for i in range(batch_size):
            #    batch_size_nn[i][:,2] = self.neural_network[:,2] -> nn_value[:,2] = self.neural_network[:,2]
            #    batch_size_optim[i].mv = self.optim.mv
            #
            '''
            from concurrent.futures import ThreadPoolExecutor

            MAX_WORKERS = thread
            while 1:
                try:
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        for i in range(batch_size):
                            executor.submit(self.fit_one_nn,batch_size_nn[i],batch_size_optim[i],x[index_batch][i],y[index_batch][i],epoch)
                    break
                except:
                   exit()   
            '''
            for i in range(batch_size):
                self.fit_one_nn(batch_size_nn[i],batch_size_optim[i],x[index_batch][i],y[index_batch][i],epoch)
            
            #print(batch_size_nn[0])
            #print(batch_size_nn[i][3][0][1][0])
            #rint(batch_size_nn[1])
            #exit()
            #
            for i in range(batch_size):
                # можна замінити на numpy
                for layer_index in range(1,self.layer_count,1):
                    #print(layer_index)
                    nn_sum[layer_index][0][2] += batch_size_nn[i][layer_index][0][2]
                    #print(optim_sum.mv[layer_index-1])
                    optim_sum.mv[layer_index-1] += batch_size_optim[i].mv[layer_index-1]
                    #print('b',batch_size_optim[i].mv[layer_index-1])
                    #print(optim_sum.mv[layer_index-1])
                    #print(optim_sum.mv[layer_index-1][0][0][0])
                #exit()
                #print(nn_sum[1][0][2])
                #print(optim_sum.mv[layer_index-1])
            #exit()
            #
            
        #
        print()
        #
        #print(nn_sum[1][0][2])
        #print(self.neural_network[1][0][2])
        for layer_index in range(1,self.layer_count,1):
            #print(layer_index)
            self.neural_network[layer_index][0][2] = nn_sum[layer_index][0][2] / float(count_label)
            self.optim.mv[layer_index-1] = optim_sum.mv[layer_index-1] / float(count_label)
        #print(self.neural_network[1][0][2])
        self.fill_weight(nn_sum,0,'w')
        self.fill_weight(optim_sum.mv,0,'m')
        #print(self.neural_network[1][0][2])

    def fit(self,x,y,batch_size,epochs,name_optimaser):
        self.optimiser_name = name_optimaser
        # кількість NN які одночасно існують
        batch_size_nn = [self.return_network_from_log(self.neural_network_log) for i in range(batch_size)]
        #
        batch_size_optim = [Optimizer(self.neural_network_log) for i in range(batch_size)]
        # створюємо змінну для рахування суми
        nn_sum = self.return_network_from_log(self.neural_network_log)
        self.fill_weight(nn_sum,0,'w')
        
        optim_sum = Optimizer(self.neural_network_log)
        self.fill_weight(optim_sum.mv,0,'m')

        count_label = len(x)
        x_vector,y_vector = [],[]
        for index_batch in range(0,count_label,batch_size):
            start = index_batch
            finish = index_batch + batch_size
            if(finish > count_label):
                finish = count_label
            x_vector.append(x[start:finish,:])
            y_vector.append(y[start:finish])

        #print(x_vector)
        #exit()
        for i in range(1,epochs,1):
            self.batch_separate(x_vector,y_vector,nn_sum,optim_sum,batch_size_nn,batch_size_optim,count_label,batch_size,i)

    def predict(self,x):
        count_label = len(x)
        y = np.zeros(count_label)
        for i in range(count_label):
            #nn_value = self.return_network_from_log(self.neural_network_log)
            #print(self.neural_network[3][0][2])
            nn_value = self.neural_network
            #print(self.neural_network[0][0][1][0,:])
            nn_value[0][0][1][0,:] = x[i,:]
            #print(x[i,:],nn_value[0][0][1][0,:],self.neural_network[0][0][1][0,:])
            
            #print(nn_value)
            self.per_all_at_once(nn_value)
            y[i] = nn_value[self.layer_count-1][0][1][0][0]            
        return y
            



#print(model.neural_network[2][0][1][0][0])
#print(model.neural_network[1][0][2])
#exit()
#print(model.optim.mv)

def OR(x,y):
  if(x==1 or y==1):
    return 1
  else:
    return 0

def XOR(x,y):
  if((x==1 or y==1) and x!=y):
    return 1
  else:
    return 0


# границі масиву, де а - довжина вектору, b - кількість векторів у наборі
a,b = 2,2000

# масив векторів х
x_train = [[np.random.randint(0,2) for i in range(a)] for j in range(b)]
#print(x_train)
# результат у
y_train = [0]*b

for i in range(b):
  # послідовність дій для створення результату у
  #sum = 0
  #for j in range(a):
  #  sum += x_train[i][j]
  
  #add error
  if(np.random.randint(0,100) == 5):
    if(XOR(x_train[i][0],x_train[i][1]) == 1):
      y_train[i] = 0
    else:
      y_train[i] = 1
  else:
    y_train[i] = XOR(x_train[i][0],x_train[i][1])

x_train = np.array(x_train)
y_train = np.array(y_train)

print('x_train: ',x_train)


a1 = Dense(2)
a2 = Dense(7,'sigmoid',a1)
a3 = Dense(7,'sigmoid',a2)
a4 = Dense(7,'sigmoid',a3)
a5 = Dense(1,'sigmoid',a4)

#print(return_network(a4))
model = Model(a5)

model.fit(x_train,y_train,batch_size = 1000,epochs = 5, name_optimaser='adam')
y = model.predict(x_train)
#print(y)

print(model.neural_network)
#print(model.neural_network[1][0][2][0][0])
#model.neural_network[1][0][2][0][0][0] = 2
#print(model.neural_network[1][0][2])
def binary_accuracy(n,y_prob,y):
  threshold = 0.51
  count = 0
  TP, FP, TN, FN = 0,0,0,0
  for i in range(n):
    if(y[i]<threshold):
      y[i] = 0
    if(y[i]>=threshold):
      y[i] = 1
    if(y[i]==y_prob[i]):
      count+=1
    if(y[i]==1):
      if(y[i]==y_prob[i]):
        TP += 1
      else:
        FP += 1
    if(y[i]==0):
      if(y[i]==y_prob[i]):
        TN += 1
      else:
        FN += 1
  Acc = count/n
  '''
  pur_a = TP/(TP+FP)
  pur_not_a = TN/(TN+FN)
  com_a = TP/(TP+FN)
  com_not_a = TN/(TN+FP)
  f1 = 2*TP/(2*TP+FP+FN)
  fpr = FP/(TN+FN)
  tnr = TN/(TN+FN)
  bAcc = (TP/(TP+FP)+TN/(TN+FN))/2.
  k = 2*(TP*TN-FN*FP)/((TP+FP)*(FP+TN)+(TP+FN)*(FN+TN))
  mcc = (TP*TN-FP*FN)/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
  BinBs = (FP+FN)/(TP+FP+FN+TN)
  '''
  print("Accuracy 				[worst: 0; best: 1]:",              Acc)
  '''
  print("AGN purity 				[worst: 0; best: 1]:",     pur_a)
  print("nonAGN precision 			[worst: 0; best: 1]:",    pur_not_a)
  print("AGN completness 			[worst: 0; best: 1]:",       com_a)
  print("nonAGN completness 			[worst: 0; best: 1]:",     com_not_a)
  print("F1  					[worst: 0; best: 1]:",		f1)
  print("FPR (false positive rate) 		[worst: 1; best: 0]:",		fpr)
  print("TNR (true negative rate) 		[worst: 0; best: 1]:",		tnr)
  print("bACC (balanced accuracy) 		[worst: 0; best: 1]:", bAcc)
  print("K (Cohen's Kappa) 			[worst:-1; best:+1]:",		k)
  print("MCC (Matthews Correlation Coef) 	[worst:-1; best:+1]:",		mcc)
  print("BinaryBS (Brierscore) 			[worst: 1; best: 0]:", BinBs)
  print()
  print()
  '''

def Simpson(a,f):
	n = len(f)
	s=0
	for i in range(1,n):
		s += (abs(a[i]-a[i-1]))*(f[i]+f[i-1])
	s*=0.5
	return s

import sklearn.metrics as skmetrics
def i_need_more_eval(path_save_eval, name, label, data_prob):
	fpr, tpr, thresholds = skmetrics.roc_curve(label, data_prob, pos_label=1)
	roc_curve_df = pd.DataFrame({"fpr": fpr, "tpr": tpr,
									"thresholds": thresholds})
	roc_curve_df = roc_curve_df[roc_curve_df['thresholds'] < 0.99]									
	roc_curve_df.to_csv(f"{path_save_eval}/{name}_roc.csv", index=False)
	print("ROC_CURVE......",name,":.......",Simpson(np.array(roc_curve_df["fpr"]),np.array(roc_curve_df["tpr"])))
	#print("ROC_CURVE......",name,":.......",Simpson(tpr,fpr))

	precision, recall, thresholds = skmetrics.precision_recall_curve(label, data_prob)
	pr_curve_df = pd.DataFrame({"precision": precision, "recall": recall, 
                                    "thresholds": np.append(thresholds, 1)})
	pr_curve_df = pr_curve_df[pr_curve_df['thresholds'] < 0.99]	
	pr_curve_df.to_csv(f"{path_save_eval}/{name}_pr.csv", index=False)
	print("PR_CURVE.......",name,":.......",Simpson(pr_curve_df["recall"],pr_curve_df["precision"]))
	#print("PR_CURVE.......",name,":.......",Simpson(precision,recall))
	max,inde=0,0
	for ii in range(len(pr_curve_df)):
		s = math.sqrt(pr_curve_df["recall"].iloc[ii]**2 + pr_curve_df["precision"].iloc[ii]**2)
		if(max < s):
			max = s
			inde = ii
	print("thresholds....",pr_curve_df["thresholds"].iloc[inde],"recall....",pr_curve_df["recall"].iloc[inde],"precision....",pr_curve_df["precision"].iloc[inde])

import matplotlib.colors as mcolors
from matplotlib import pyplot as plt
c=np.append(list(mcolors.TABLEAU_COLORS),list(mcolors.BASE_COLORS))

def ROC_picture(path_save_eval,name,classif):
	fontsize_sub = 50
	fontsize_label = 24
	fontsizr_param = 24
	fontsize_legend = 20
	size = (12,11)

	fig1 = plt.figure()
	ax1 = fig1.add_subplot(1,1,1)
	#fig1.suptitle("", fontsize=fontsize_sub)
	ax1.set_xlabel("Probability thresholds", fontsize=fontsize_label)
	ax1.set_ylabel("Precision", fontsize=fontsize_label)
	ax1.tick_params(axis='x', labelsize=fontsizr_param)
	ax1.tick_params(axis='y', labelsize=fontsizr_param)
	fig1.set_size_inches(size)

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1,1,1)
	#fig2.suptitle("", fontsize=fontsize_sub)
	ax2.set_xlabel("Probability thresholds", fontsize=fontsize_label)
	#ax2.set_ylabel("Completeness", fontsize=fontsize_label)
	ax2.set_ylabel("Recall", fontsize=fontsize_label)
	ax2.tick_params(axis='x', labelsize=fontsizr_param)
	ax2.tick_params(axis='y', labelsize=fontsizr_param)
	fig2.set_size_inches(size)

	fig3 = plt.figure()
	ax3 = fig3.add_subplot(1,1,1)
	#fig3.suptitle("", fontsize=fontsize_sub)
	#ax3.set_xlabel("Completeness", fontsize=fontsize_label)
	ax3.set_xlabel("Recall", fontsize=fontsize_label)
	ax3.set_ylabel("Precision", fontsize=fontsize_label)
	ax3.tick_params(axis='x', labelsize=fontsizr_param)
	ax3.tick_params(axis='y', labelsize=fontsizr_param)
	fig3.set_size_inches(size)

	fig4 = plt.figure()
	ax4 = fig4.add_subplot(1,1,1)
	#fig4.suptitle("", fontsize=fontsize_sub)
	ax4.set_xlabel("FPR", fontsize=fontsize_label)
	ax4.set_ylabel("TPR", fontsize=fontsize_label)
	ax4.tick_params(axis='x', labelsize=fontsizr_param)
	ax4.tick_params(axis='y', labelsize=fontsizr_param)
	fig4.set_size_inches(size)
	
	index=1
	for cl in classif:
		data_pr = pd.read_csv(f"{path_save_eval}/{name}_{cl}_pr.csv", sep=",", header=0)
		#ax1.plot(data_pr['thresholds'],data_pr['precision'],c=c[index],label=cls_name[index-1])
		ax1.plot(data_pr['thresholds'],data_pr['precision'],c=c[index],label=cl)
		index+=1

	index=1
	for cl in classif:
		data_pr = pd.read_csv(f"{path_save_eval}/{name}_{cl}_pr.csv", sep=",", header=0)		
		ax2.plot(data_pr['thresholds'],data_pr['recall'],c=c[index],label=cl)
		index+=1

	index=1
	for cl in classif:
		data_pr = pd.read_csv(f"{path_save_eval}/{name}_{cl}_pr.csv", sep=",", header=0)
		ax3.plot(data_pr['precision'],data_pr['recall'],c=c[index],label=cl)
		index+=1

	index=1
	for cl in classif:
		data_roc = pd.read_csv(f"{path_save_eval}/{name}_{cl}_roc.csv", sep=",", header=0)
		ax4.plot(data_roc['fpr'],data_roc['tpr'],c=c[index],label=cl)
		index+=1



	ax1.legend(loc=4,prop={'size': fontsize_legend})
	ax2.legend(loc=3,prop={'size': fontsize_legend})
	ax3.legend(loc=3,prop={'size': fontsize_legend})
	ax4.legend(loc=4,prop={'size': fontsize_legend})
	fig1.savefig(f"{path_save_eval}/{name}_pr_th.png")
	fig2.savefig(f"{path_save_eval}/{name}_rc_th.png")
	fig3.savefig(f"{path_save_eval}/{name}_pr_rc.png")
	fig4.savefig(f"{path_save_eval}/{name}_roc.png")
	plt.close(fig1)
	plt.close(fig2)
	plt.close(fig3)
	plt.close(fig4)

print(y,y_train)
eval(y_train,y,len(x_train))


'''
class NN_one(Optimizer):
    layer_count=0

    #self.network_weight_value = {"layer_1" : ''}
    #self.network_weight_grad = {"layer_1" : ''}
    #self.network_activation_function = {"layer_1": 'linear'}

    def __init__(self):
      pass

    def __init__(self,log,network_weight_value):
      self.network_log_read(log)
      self.network_weight_value_read(network_weight_value)

    def Input(self, features_count):
      # створює dictionary для збереження інформації про кількість нейронів у кожному з шарів
      self.network_neuron_count = {"layer_0" : features_count}
      # створює dictionary для збереження значень кожного нейрона
      self.network_neuron_value = {"layer_0" : np.zeros((1,features_count))}
      # створює dictionary для збереження значення ваги переходу до наступного нейрона
      self.network_weight_value = {"layer_1" : ''}
      # 
      self.network_weight_grad = {"layer_1" : ''}
      # створює dictionary для збереження назв фунцій активації
      self.network_activation_function = {"layer_1": 'linear'}


    def Dense(self, layer_count_neuron, activation_function_name):
      #
      self.layer_count += 1
      # додає значення кількості нейронів у шарі до загального значення
      self.network_neuron_count[f'layer_{self.layer_count}'] = layer_count_neuron
      # додає значення ваги переходу кожного нейрону данного ряду, до кожного наступного
      self.network_weight_value[f'layer_{self.layer_count}'] = np.ones((layer_count_neuron,self.network_neuron_count[f'layer_{self.layer_count-1}']))
      #
      self.network_weight_grad[f'layer_{self.layer_count}'] = np.ones((layer_count_neuron,self.network_neuron_count[f'layer_{self.layer_count-1}']))
      # додає новий рядок для збереження значень нейронів
      self.network_neuron_value[f'layer_{self.layer_count}'] = np.zeros((2,layer_count_neuron))
      # додає назву функції активації для кожного ряду
      self.network_activation_function[f'layer_{self.layer_count}'] = activation_function_name

    def network_log_write(self):
        #треба через функцію поміняти всі ключові слова на назви функцій активації
        log = {'NaN': self.network_neuron_count['layer_0']}
        for i in range(1,self.layer_count,1):
           log[self.network_activation_function[f'layer_{i}']] = self.network_neuron_count[f'layer_{i}'] 
        return log
    
    def network_log_read(self,log):
        index_layer = 0
        last_name = ''
        for activation_function_name in log.keys():
            
            column_name = f'layer_{index_layer}'
            
            if(last_name == ''):            
                self.network_neuron_value[column_name] = np.zeros((1,log[activation_function_name]))
                self.network_neutron_count[column_name] = log[activation_function_name]
            else:
                self.network_weight_value[column_name] = np.ones((log[activation_function_name],log[last_name]))
                self.network_weight_grad[column_name] = np.ones((log[activation_function_name],log[last_name]))
                self.network_neuron_value[column_name] = np.zeros((2,log[activation_function_name]))
                self.network_neutron_count[column_name] = log[activation_function_name]
                self.network_activation_function[column_name] = activation_function_name
                
            self.layer_count = index_layer

            last_name = activation_function_name

            index_layer += 1

    def network_weight_value_read(self,input_weight):
        for index_layer in range(1,len(self.network_weight_value.keys())+1,1):
            self.network_weight_value[f'layer_{index_layer}'] = input_weight[f'layer_{index_layer}']

    def network_weight_value_write(self):
        output_weight = {'layer_1': ''}
        for index_layer in range(1,self.layer_count + 1,1):
            output_weight[f'layer_{index_layer}'] = self.network_weight_value[f'layer_{index_layer}']
        return output_weight
    
    def network_weight_value_null(self,value):
        for index_layer in range(1,len(self.network_weight_value.keys())+1,1):
            self.network_weight[f'layer_{index_layer}'].fill(value)

    def set_param(self,optimizer_name,y_label):
        self.optim = Optimizer(self.network_log_write)
        self.optimizer_name = optimizer_name
        self.y = y_label

    def perseptron(self,layer_index,neuron_index):
      if(layer_index > 0 and layer_index <= self.layer_count):
        if(neuron_index >= 0 and neuron_index < self.network_neuron_count[f'layer_{layer_index}']):
          #afn = self.network_activation_function[f'layer_{layer_index}']
          sum = self.network_weight_value[f'layer_{layer_index}'][neuron_index, : ].dot(self.network_neuron_value[f'layer_{layer_index-1}'][0,:])
          #print(sum)
          #print(self.network_neuron_value[f'layer_{layer_index}'][0,neuron_index])
          #print(self.network_activation_function[f'layer_{layer_index}'])
          #print(activation_function(self.network_activation_function[f'layer_{layer_index}'],sum))
          self.network_neuron_value[f'layer_{layer_index}'][0,neuron_index] = ActivationFunction(self.network_activation_function[f'layer_{layer_index}'],sum)
          self.network_neuron_value[f'layer_{layer_index}'][1,neuron_index] = ActivationFunction(f"derivative_{self.network_activation_function[f'layer_{layer_index}']}",sum)

    def per_all_at_once(self):
      for layer_index in range(1,self.layer_count+1,1):
        for j in range(self.network_neuron_count[f'layer_{layer_index}']):
          self.perseptron(layer_index,j)

    def perceptron_grad(self,layer_index,i,j):
        index = f"layer_{layer_index}"
        if(layer_index > 0):
            if(layer_index < self.layer_count):
                self.network_weight_grad[index][i][j] = (self.network_neuron_value[f"layer_{layer_index-1}"][0][j]/self.network_neuron_value[index][0][j])*self.network_neuron_value[index][1][i]*self.network_weight_value[f'layer_{layer_index+1}'][:,i].dot(self.network_weight_grad[f'layer_{layer_index+1}'][:,j])
            elif(layer_index == self.layer_count):
                self.network_weight_grad[index][i][j] = self.network_neuron_value[index][1][i]*self.network_neuron_value[f"layer_{layer_index-1}"][0][j]
            
    def grad_all_at_once(self):
        for layer_index in range(self.layer_count,1,-1):
            for i in range(self.network_neuron_count[f'layer_{layer_index}']):
                for j in range(self.network_neuron_count[f'layer_{layer_index-1}']):
                    self.perceptron_grad(layer_index,i,j)

    def backpropagation(self,epoch):
        self.grad_all_at_once()
        self.optim.time_step_epoch = epoch
        for layer_index in range(self.layer_count,1,-1):
            for i in range(self.network_neuron_count[f'layer_{layer_index}']):
                for j in range(self.network_neuron_count[f'layer_{layer_index-1}']):
                    #print(LossFunction('derivative_square',self.network_neuron_value[f'layer_{self.layer_count}'][0][0],self.y))
                    #exit()
                    self.network_weight_value[f'layer_{layer_index}'][i][j] +=  LossFunction(name = 'derivative_square',
                                                                                             y_prob = self.network_neuron_value[f'layer_{self.layer_count}'][0][0],
                                                                                             y = self.y)*self.optim(name = self.optimizer_name,
                                                                                                                    grad_value = self.network_weight_grad[f'layer_{layer_index}'][i][j],
                                                                                                                    i=i,
                                                                                                                    j=j)
    def fit_NN_one(self,x,y,epochs):
        self.set_param(self.optimization_function,y)
        print(self.network_neuron_value)
        for i in range(self.network_neuron_count['layer_0']):
            self.network_neuron_value["layer_0"][0,i] = x[i]
        for epoch in range(epochs):
            self.per_all_at_once()
            self.backpropagation(epoch = epoch)
        self.per_all_at_once()
        return LossFunction('square',self.network_neuron_value[f'layer_{self.layer_count}'][0][0],self.y)
'''

'''
a = NN_one(7)
a.Dense(7,'linear')
a.Dense(7,'linear')
a.Dense(7,'linear')
a.Dense(1,'sigmoid')
#print(a.network_weight_value)
a.fit([9,8,7,6,2,3,5],1)
b = [NN_one(7) for i in range(100)]
b[0].y = 10
print(b[1].y)
print(b[0].y)
#print(a.network_weight_value)
#print(a.network_neuron_value)
#print(a.network_weight_grad)
#print(a.network_weight_value['layer_1'][2][3])
'''
# визначення learning_rate, loss_function
'''
class NN_multiple():

    def __init__(self,class_sample,optimization_function,epochs,batch_size):
        self.class_sample = class_sample
        self.optimization_function = optimization_function
        self.count_label = len(self.x_label)
        self.epochs = epochs
        self.batch_size = batch_size

    def batch_separate(self,network_weight_value,batch_size,epoch = 1,thread = 4):
        # зберігаємо макет структури НМ
        log = self.class_sample.network_log_write()
        # кількість класів які одночасно існують       
        batch_size_class_nn = [NN_one(log,network_weight_value) for i in range(batch_size)]
        # створюємо змінну для рахування суми
        self.class_sample.network_weight_value_null(0)
        network_weight_sum = self.class_sample.network_weight_value_write()
        
        mv_sum = self.class_sample.optim.mv

        for index_batch in range(0,self.count_label,batch_size):
            x_vector = self.x_label[index_batch*batch_size:(index_batch+1)*batch_size,:]
            y_vector = self.y_label[index_batch*batch_size:(index_batch+1)*batch_size]

            MAX_WORKERS = thread

            from concurrent.futures import ThreadPoolExecutor
            if (batch_size // thread == 0):
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    for i in range(0,batch_size,MAX_WORKERS):
                        for j in range(MAX_WORKERS):
                            executor.submit(batch_size_class_nn[i+j].fit_NN_one,x_vector[i+j,:],y_vector[i+j],epoch)    
            else:
                temp_batch_size = batch_size - (batch_size // thread)
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    for i in range(0,batch_size,MAX_WORKERS):
                        for j in range(MAX_WORKERS):
                            executor.submit(batch_size_class_nn[i+j].fit_NN_one,x_vector[i+j,:],epoch)    
                    for i in range(temp_batch_size,batch_size,1):
                        executor.submit(batch_size_class_nn[i].fit_NN_one,x_vector[i,:],y_vector[i+j],epoch)

            for i in range(batch_size):
                for name_layer in self.class_sample.network_weight_value.keys():
                    network_weight_sum[name_layer] += batch_size_class_nn[i].network_weight_value[name_layer]
                    mv_sum[name_layer] += batch_size_class_nn[i].optim.mv[name_layer]
                
                batch_size_class_nn[i].network_weight_value_read(network_weight_value)
        
        for name_layer in self.class_sample.network_weight_value.keys():
            network_weight_sum[name_layer] /= self.count_label
        
        return network_weight_sum

    
    def fit_NN_multiple(self,x,y):
        self.x_label = x
        self.y_label = y
        #self.class_sample.network_weight_value_null(1)
        network_weight_value = self.class_sample.network_weight_value_write()
        for i_epoch in range(1,self.epochs+1,1):
            network_weight_value = self.batch_separate(network_weight_value = network_weight_value,
                                                        batch_size = self.batch_size,
                                                        epoch = i_epoch)

'''

'''
a = NN_one(7)
a.Dense(7,'linear')
a.Dense(7,'linear')
a.Dense(7,'linear')
a.Dense(1,'sigmoid')
b = NN_multiple(a,'adam',10,1024)
b.fit_NN_multiple(x,y)




'''