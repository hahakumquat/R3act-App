#!flask/bin/python
from flask import Flask, request, jsonify
import pandas
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

def wrangle_data(filename):
    result, data = read_data(filename)
    result, data = trim_data(result, data)
    result, data = standardize_data(result, data)
    result['data'] = data
    return result

def read_data(filename):
    keys = ['Age', 'Height', 'Weight', 'Gender']
    with open(filename) as f:
        ## collect data from file
        result = {}
        result['filename'] = filename
        for i in range(8):
            next(f)
        for i in keys:
            tmp = f.readline()
            result[i] = tmp[(tmp.index(' ') + 1):-1]
        for i in range(4):
            next(f)
        data = []
        for r in f:
            d = r[:-1].split(', ')
            data.append([float(i) for i in d])
    return result, data

def standardize_data(result, data):
    x_med = np.median([d[1] for d in data])
    y_med = np.median([d[2] for d in data])
    z_med = np.median([d[3] for d in data])     
    result['duration'] = (data[-1][0] - data[0][0]) / time_unit
    ## standardizes Y data by median and X time to 0 second start
    data = list(map(lambda d : 
                    [(d[0] - data[0][0]) / time_unit, 
                     d[1] - x_med, 
                     d[2] - y_med, 
                     d[3] - z_med], 
                    data))
    return result, data

def trim_data(result, data):
    x_data = [d[1] for d in data]
    x_min = min(x_data)
    x_max = max(x_data)  

    y_data = [d[2] for d in data]
    y_min = min(y_data)
    y_max = max(y_data)

    z_data = [d[3] for d in data]
    z_min = min(z_data)
    z_max = max(z_data)

    del x_data
    del y_data
    del z_data

    ## cuts off start and end
    data = trim_quantiles(data, quantile_trim)

    ## find threshold amount to trim
    threshold = min([abs(x_max - x_min), abs(y_max - y_min), abs(z_max - z_min)]) * threshold_epsilon
    (l_trim, r_trim) = trim_threshold(data, threshold)
    l_trim = int(max([l_trim - len(data) * margin, 0]))
    r_trim = int(min([r_trim + len(data) * margin, len(data)]))
    return result, data[l_trim:r_trim]

def trim_quantiles(data, quantiles):
    return data[int(len(data) * quantiles[0]):int(len(data) * quantiles[1])]

def trim_threshold(data, threshold):
    l_trim = 0
    while l_trim < len(data) - 2:
        # dt = data[l_trim][0] - data[l_trim + 1][0]
        dt = 1
        dx = data[l_trim][1] - data[l_trim + 1][1]
        dy = data[l_trim][2] - data[l_trim + 1][2]
        dz = data[l_trim][3] - data[l_trim + 1][3]
        if (abs(dx/dt) > threshold
        and abs(dy/dt) > threshold
        and abs(dz/dt) > threshold):
            break
        else:
            l_trim += 1
            
    r_trim = len(data) - 1
    while r_trim > l_trim:
        # dt = data[r_trim][0] - data[r_trim - 1][0]
        dt = 1
        dx = data[r_trim][1] - data[r_trim - 1][1]
        dy = data[r_trim][2] - data[r_trim - 1][2]
        dz = data[r_trim][3] - data[r_trim - 1][3]
        if (abs(dx/dt) > threshold
        and abs(dy/dt) > threshold
        and abs(dz/dt) > threshold):
            break
        else:
            r_trim -= 1
            
    return (l_trim, r_trim)

def plot_data(data, title=None):
    n = len(data)
    Xs = [data[i][0] for i in range(n)]
    Ys = [data[i][1] for i in range(n)]
    plt.title(title)
    plt.plot(Xs, Ys, c="r")
    Ys = [data[i][2] for i in range(n)]
    plt.plot(Xs, Ys, c="g")
    Ys = [data[i][3] for i in range(n)]
    plt.plot(Xs, Ys, c="b")
    plt.show()

## edward wrote this, michael wrote everything else
def get_files(root_dir):
    result = [root_dir + file for file in os.listdir(root_dir) if not os.path.isdir(root_dir+file)]
    for file in [file for file in os.listdir(root_dir) if os.path.isdir(root_dir+file)]:
        result = result + get_files(root_dir + file + '/')
    return result

def load(root='./MobiFall/', plot=False):
    root_dir = root
    categories = {}
    for file in [file for file in get_files(root_dir) if file[-4:] == '.txt' and file[-6] == '_' 
                 and ('acc' in file)]:
        prefix = os.path.basename(file)[0:3]
        if prefix not in categories:
            obj = []
            categories[prefix] = obj
        result = wrangle_data(file)
        categories[prefix].append(result)
        if plot:
            plot_data(result['data'], file)
    return categories

def bucket(data):
    quantiles = [(i + 1) * duration / n_buckets for i in range(n_buckets)]
    buckets = [[quantiles[i], 0, 0, 0] for i in range(n_buckets)]
    ctr = 0
    idx = 0
    for i in range(len(data['data'])):
        if quantiles[idx] < data['data'][i][0]:
            for j in range(len(buckets[idx])-1):
                buckets[idx][j+1] /= ctr
            idx += 1
            ctr = 0
            if idx >= n_buckets:
                break
        ctr += 1
        for j in range(len(buckets[idx])-1):
            buckets[idx][j+1] += data['data'][i][j+1]
    while idx < n_buckets - 1:
        for j in range(len(buckets[idx])-1):
            buckets[idx + 1][j+1] = buckets[idx][j+1]
        idx += 1
    data['data'] = buckets
    return data

def flatten(data):
    lst = []
    for k in sorted(data.keys()):
        if k != 'data' and k != 'filename':
            try:
                lst.append(float(data[k]))
            except:
                lst.append(1 if data[k] == 'Male' else 0)
    for d in data['data']:
        lst = lst + d
    return lst

threshold_epsilon = 0.05
margin = 0.2
time_unit = 1000000000
duration = 5
quantile_trim = [0.02, 0.98]
n_buckets = 30

categories = load('MobiFall/', False)

for cat in categories:
    for i in range(len(categories[cat])):
        categories[cat][i] = bucket(categories[cat][i]) 
        categories[cat][i] = flatten(categories[cat][i])

## building training and validation data

X_train = []
Y_train = []
X_val = []
Y_val = []
for cat in categories:
    for i in range(len(categories[cat])):
        split = int(len(categories[cat]) * 0.6)
        X_train = X_train + categories[cat][:split]
        X_val = X_val + categories[cat][split:]
        if cat in ['FOL', 'FKL']:
            Y_val = Y_val + (['Fall'] * (len(categories[cat]) - split))
            Y_train = Y_train + (['Fall'] * split)
        else:
            Y_val = Y_val + (['Not Fall'] * (len(categories[cat]) - split))
            Y_train = Y_train + (['Not Fall'] * split)

rfc = RandomForestClassifier()
rfc.fit(X_train, Y_train)

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get_tasks():
    result = rfc.predict
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
