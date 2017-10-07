# predict PM2.5 from previous 9 hours data
# Model 1 : L = (y - (b + WiXi)) ** 2 )
# By Junhong Yang 10/5/2017

import csv

#  load data


# set up initial value of weights and bias and put it into an array
# [w1, w2........w9]
# bias
weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
bias = 2


optimization = True

# initialize threshold of optimization
threshold = 1

# set up initial learning_rate
learning_rate = 1

# set up bias gradient and weights gradient array
bias_gradient = 0
weights_gradientset = [0,0,0,0,0,0,0,0,0]

# save the sum of previous weight gradient square (previous_WeightGS) for Adagrad
# save the sum of previous bias gradient square (previous_BiasGS) for Adagrad
previous_WeightGS = [0,0,0,0,0,0,0,0,0]
previous_BiasGS = 0



workbook_name = "train.csv"
#

output = []
# Model 1 y = WiXi + b
with open(workbook_name, 'r') as csvfile:
    reader = csv.reader(csvfile)
    step = 0
    while optimization:
        # update the weights for next step
        step += 1
        print("step {}:  weights gradient : {} {}".format(step, weights_gradientset, bias_gradient))

        # update the weights based on W(t+1) = W - LR * Gradient(t) / (previous_WeightGS) ** 0.5
        for weightid in range(len(weights)):

            # save the gradient square in the last step
            previous_WeightGS[weightid] += weights_gradientset[weightid] ** 2

            # update the weights
            if abs(weights_gradientset[weightid]) > threshold:
                weights[weightid] -= weights_gradientset[weightid] * learning_rate / (previous_WeightGS[weightid] ** 0.5)

        # save the gradient square of bias in the last step
        previous_BiasGS += bias_gradient ** 2

        # update the bias
        if abs(bias_gradient) > threshold:
            bias -= bias_gradient * learning_rate / (previous_BiasGS ** 0.5)

        # clean the gradient for weights and bias
        weights_gradientset = [0,0,0,0,0,0,0,0,0]
        bias_gradient = 0

        # return to the top of the file
        csvfile.seek(0)

        # separate the training data sheet into training and validation
        cutpoint = 200
        row_number = 0
        for row in reader:
            if "PM2.5" in row:  # do following calculation if in PM2.5 row
                row_number += 1

                # separate training set and validation set
                if row_number <= cutpoint:
                    starting_point = row.index("PM2.5") + 1
                    for i in range(starting_point, len(row)):  # extract the PM2.5 data starting from the starting point
                        if i + 9 < len(row):  # make sure the 9 data you get is in the same day
                            function_set = 0  # set up function set
                            values = []

                            for data_col in range(i, i + 9):  # load the data of previous 9 hours PM2.5 and save it to value
                                values.append(int(row[data_col]))

                            for paramater_id in range(len(weights)):  # calculate the function set
                                function_set += weights[paramater_id] * values[paramater_id]

                            function_set += bias
                            actual_PM = int(row[i + 9])

                            # update the array of gradients for every sample
                            for id in range(9):
                                weights_gradientset[id] += (-2) * (actual_PM - function_set) * values[id]

                            bias_gradient += (-2) * (actual_PM - function_set)

        # gradient should be less than 2
        if abs(max(weights_gradientset)) <= threshold and abs(bias_gradient) <= threshold and abs(min(weights_gradientset)) <= threshold:
            optimization = False

    # model validation
    total_error = 0
    data_num = 0

    # return to the top of the file
    csvfile.seek(0)
    cutting_point = 200
    row_number = 0
    for row in reader:
        if "PM2.5" in row:
            row_number += 1
            if row_number > cutting_point:
                starting_point = row.index("PM2.5") + 1
                for i in range(starting_point, len(row)):  # extract the PM2.5 data starting from the starting point
                    if i + 9 < len(row):  # make sure the 9 data you get is in the same day
                        data_num += 1
                        function_set = 0  # set up function set
                        values = []

                        for data_col in range(i, i + 9):  # load the data of previous 9 hours PM2.5 and save it to value
                            values.append(int(row[data_col]))

                        for paramater_id in range(len(weights)):  # calculate the function set
                            function_set += weights[paramater_id] * values[paramater_id]

                        # calculate the error for every data point
                        function_set += bias
                        actual_PM = int(row[i + 9])
                        total_error += (actual_PM - function_set) ** 2

    # calculate the average error
    Ave_error = total_error / data_num

output = weights
output.append(bias)

header = ["weight1", "weight2", "weight3", "weight4", "weight5", "weight6", "weight7", "weight8", "weight9", "bias"]
print("The average error of model one is: {}   output = {}".format(Ave_error, output))
print(type(output))
with open("model1.csv", 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerow(output)
    writer.writerow(["Average error"])
    writer.writerow([Ave_error])

