import numpy as np
import matplotlib.pyplot as plt


def read_in_vcm(file_name, show_plot=False):
    # Read out vcm files
    path = f'../messdaten/{file_name}.vcm'

    with open(path, 'r') as file:
        # Skip file header
        for i in range(0, 22):
            file.readline()

        data_points = []

        # Read in data points from file
        value = file.readline().strip()
        while value == 'NAN' or value.count('.') == 0:  # Don't allow float which ends the the list
            if value != 'NAN':
                data_points.append(int(value))
            else:
                data_points.append('NAN')

            value = file.readline().strip()

        # generate x-Axis values with 0.1s intervals
        x_axis = [i/10 for i in range(0, len(data_points))]

        print(data_points.count('NAN'))

        # Remove 'NAN' values
        nan_times = 0
        for i in range(0, len(data_points) - data_points.count('NAN')):
            if data_points[i - nan_times] == 'NAN':
                data_points.pop(i - nan_times)
                x_axis.pop(i - nan_times)
                nan_times += 1

        if show_plot:
            plt.plot(x_axis, data_points)
            plt.show()

        return x_axis, data_points


def generate_csv(file_name, x_axis, data_points):
    # generate csv file
    path = f'../messdaten/{file_name}.csv'
    with open(path, 'w') as file:
        file.write('time, position \n')  # add header for pgfplots
        for i in range(0, len(data_points)):
            file.write(f'{x_axis[i]},{data_points[i]} \n')
        file.flush()


harmonisch = read_in_vcm('Versuch2')
gleich_phasig = read_in_vcm('Versuch3.1')
gegen_phasig = read_in_vcm('Versuch3.2')
schwebung = read_in_vcm('Versuch3.3')

# Write out in csv for loading with pgfplots
generate_csv('harmonisch', harmonisch[0], harmonisch[1])

# Exemplary usage for data analysis
data = np.array(harmonisch[1])
print(data.max())
print(data.mean())

