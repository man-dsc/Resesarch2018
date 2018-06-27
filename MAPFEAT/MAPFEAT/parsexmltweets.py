# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:51:32 2018

@author: dicke
"""

import csv

with open('', 'r') as f1:
    reader = csv.reader(f1)
    dataset = []
    for row in reader:
        if row != '':
            if '<tweet' not in row:
                if '<auth' not in row:
                    if row != ' ':
                        dataset.append(row)
with open('', 'w') as f2:
    writer = csv.writer(f2)
    for row in dataset:
        writer.writerow(row)
        
    