import matplotlib.pyplot as plt


def create_plots(data, file_path) -> None:
    data[data.columns[6]] = data[data.columns[6]].astype(float) - data[data.columns[6]].min()
    plt.figure(figsize=(10, 6))
    for column in data.columns[:3]:
        plt.plot(data[data.columns[3]], data[column], label=column)
    plt.legend()
    plt.savefig(f'{file_path}/gyro.png')

    # Plot x and y axes
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[0]], data[data.columns[1]], label='x vs y')
    plt.legend()
    plt.savefig(f'{file_path}/gyro_xy.png')

    # Plot x and z axes
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[0]], data[data.columns[2]], label='x vs z')
    plt.legend()
    plt.savefig(f'{file_path}/gyro_xz.png')

    # Plot y and z axes
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[1]], data[data.columns[2]], label='y vs z')
    plt.legend()
    plt.savefig(f'{file_path}/gyro_yz.png')

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[data.columns[0]], data[data.columns[1]], data[data.columns[2]])
    ax.set_xlabel(data.columns[0])
    ax.set_ylabel(data.columns[1])
    ax.set_zlabel(data.columns[2])
    plt.savefig(f'{file_path}/gyro_scatter3d.png')

    # Plot accel x, y, and z
    plt.figure(figsize=(10, 6))
    for column in data.columns[3:6]:  # Change the range to 3:6
        plt.plot(data[data.columns[3]], data[column], label=column)
    plt.legend()
    plt.savefig(f'{file_path}/accel.png')  # Change the file name

    # Plot x and y axes of accelerometer
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[3]], data[data.columns[4]], label='x vs y')  # Change the columns
    plt.legend()
    plt.savefig(f'{file_path}/accel_xy.png')  # Change the file name

    # Plot x and z axes of accelerometer
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[3]], data[data.columns[5]], label='x vs z')  # Change the columns
    plt.legend()
    plt.savefig(f'{file_path}/accel_xz.png')  # Change the file name

    # Plot y and z axes of accelerometer
    plt.figure(figsize=(10, 6))
    plt.plot(data[data.columns[4]], data[data.columns[5]], label='y vs z')  # Change the columns
    plt.legend()
    plt.savefig(f'{file_path}/accel_yz.png')  # Change the file name

    # 3D scatter plot of accelerometer data
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data[data.columns[3]], data[data.columns[4]], data[data.columns[5]])
    ax.set_xlabel(data.columns[3])
    ax.set_ylabel(data.columns[4])
    ax.set_zlabel(data.columns[5])
    plt.savefig(f'{file_path}/accel_scatter3d.png')  # Change the file name
