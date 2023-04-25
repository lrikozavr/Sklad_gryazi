# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import math
def activation_function(name,value):
       
    # функція активації
    def sigmoid(x):
      return 1/(1+math.exp(-x))
    
    def linear(x):
      return x
    # деривативна функція активації
    def derivative_sigmoid(x):
      return sigmoid(x) * (1 - sigmoid(x))
    
    def derivative_linear(x):
      return 1
    
    match name:
      case 'linear':
        return linear(value)
      case 'sigmoid':
        return sigmoid(value)
      case 'derivative_linear':
        return derivative_linear(value)
      case 'derivative_sigmoid':
        return derivative_sigmoid(value)
      case _:
          Exception('Fuck off')

def LossFunction(name,y_prob,y):
    
    def square(y_prob,y):
        return 0.5*pow(y_prob-y,2)
    
    def derivative_square(y_prob,y):
        return y_prob-y
    
    match name:
       case 'square':
          return square(y_prob,y)
       case 'derivative_square':
          return derivative_square(y_prob,y)
#print(activation_function('sigmoid',10.0))
#print(activation_function('linear',10.0))

class Optimizer():
    time_step_epoch = 1
    
    def __init__(self):
        pass
    
    def __init__(self,log):
        last_name = ''
        index_layer = 0
        for key in log.keys():
            name = f'layer_{index_layer}'
            if(last_name==''):
                self.m = {name: np.zeros((1,log[key]))}
                self.v = {name: np.zeros((1,log[key]))}
            else:
                self.m[name] = np.zeros((log[last_name],log[key]))
                self.v[name] = np.zeros((log[last_name],log[key]))
            last_name = key
            index_layer += 1

    def adam(self,layer_index,i,j,grad_value,b1 = 0.9,b2 = 0.99,alpha = 0.001,e = 1e-10):
        self.m1[f'layer_{layer_index}'][i][j] = b1*self.m[f'layer_{layer_index}'][i][j] + (1-b1)*grad_value
        self.v1[f'layer_{layer_index}'][i][j] = b2*self.v[f'layer_{layer_index}'][i][j] + (1-b2)*grad_value**2
        mt = self.m1[f'layer_{layer_index}'][i][j]/(1-pow(b1,self.t))
        vt = self.v1[f'layer_{layer_index}'][i][j]/(1-pow(b2,self.t))
        return -alpha*mt/(pow(vt,0.5) + e)

    def grad(grad_value,alpha = 0.001,e = 1e-10):
        return -alpha*grad_value

    def optimazer(self,name,grad_value,layer_index,i,j):
        match name:
          case 'adam':
              return self.adam(layer_index,i,j)
          case 'grad':
              return self.grad(grad_value)

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
          self.network_neuron_value[f'layer_{layer_index}'][0,neuron_index] = activation_function(self.network_activation_function[f'layer_{layer_index}'],sum)
          self.network_neuron_value[f'layer_{layer_index}'][1,neuron_index] = activation_function(f"derivative_{self.network_activation_function[f'layer_{layer_index}']}",sum)

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
    def fit(self,x,y,epochs):
        self.set_param(self.optimization_function,y)
        print(self.network_neuron_value)
        for i in range(self.network_neuron_count['layer_0']):
            self.network_neuron_value["layer_0"][0,i] = x[i]
        for epoch in range(epochs):
            self.per_all_at_once()
            self.backpropagation(epoch = epoch)
        self.per_all_at_once()
        return LossFunction('square',self.network_neuron_value[f'layer_{self.layer_count}'][0][0],self.y)



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

# визначення learning_rate, loss_function

class NN_multiple(NN_one):

    def __init__(self,class_sample,x,y,optimization_function):
        self.class_sample = class_sample
        self.x_label = x
        self.y_label = y
        self.optimization_function = optimization_function
        self.count_label = len(self.x_label)

    def batch_separate(self,network_weight_value,batch_size,thread = 4):
        epoch = 1
        # зберігаємо макет структури НМ
        log = self.class_sample.network_log_write()
        # кількість класів які одночасно існують       
        batch_size_class_nn = [NN_one(log,network_weight_value) for i in range(batch_size)]
        # створюємо змінну для рахування суми
        self.class_sample.network_weight_value_null(0)
        network_weight_sum = self.class_sample.network_weight_value_write()

        for index_batch in range(0,self.count_label,batch_size):
            x_vector = self.x_label[index_batch*batch_size:(index_batch+1)*batch_size,:]
            y_vector = self.y_label[index_batch*batch_size:(index_batch+1)*batch_size]

            MAX_WORKERS = thread

            from concurrent.futures import ThreadPoolExecutor
            if (batch_size // thread == 0):
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    for i in range(0,batch_size,MAX_WORKERS):
                        for j in range(MAX_WORKERS):
                            executor.submit(batch_size_class_nn[i+j].fit,x_vector[i+j,:],y_vector[i+j],epoch)    
            else:
                temp_batch_size = batch_size - (batch_size // thread)
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    for i in range(0,batch_size,MAX_WORKERS):
                        for j in range(MAX_WORKERS):
                            executor.submit(batch_size_class_nn[i+j].fit,x_vector[i+j,:],epoch)    
                    for i in range(temp_batch_size,batch_size,1):
                        executor.submit(batch_size_class_nn[i].fit,x_vector[i,:],y_vector[i+j],epoch)

            for i in range(batch_size):
                for name_layer in self.class_sample.network_weight_value.keys():
                    network_weight_sum[name_layer] += batch_size_class_nn[i].network_weight_value[name_layer]
                
                batch_size_class_nn[i].network_weight_value_read(network_weight_value)
        
        for name_layer in self.class_sample.network_weight_value.keys():
            network_weight_sum[name_layer] /= self.count_label

    






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
  if(np.random.randint(0,20) == 5):
    if(OR(x_train[i][0],x_train[i][1]) == 1):
      y_train[i] = 0
    else:
      y_train[i] = 1
  else:
    y_train[i] = OR(x_train[i][0],x_train[i][1])
