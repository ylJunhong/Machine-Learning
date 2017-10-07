# Use Model 1 to do prediction
# created by Junhong Yang in 10/7/17

import csv

# extract weights and bias
with open("model1_output.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    header = reader.next()
    weights = reader.next()
    bias = weights[-1]
    weights = weights[:-1]


with open("test.csv", 'r') as csvfile:
    with open("output.csv", 'wb') as f:
        writer = csv.writer(f)
        reader = csv.reader(csvfile)
        id_predict = []
        writer.writerow(["id", "value"])
        for row in reader:
            if "PM2.5" in row:
                values = []
                prediction = 0
                output_list = []

                # save id
                output_list.append(row[0])

                # save data of previous 9 hours
                starting_point = row.index("PM2.5") + 1
                values = row[starting_point:]

                # calculate the output
                for i in range(len(values)):
                    prediction += float(values[i]) * float(weights[i])
                prediction += float(bias)
                output_list.append(str(prediction))

                # write id and output
                writer.writerow(output_list)