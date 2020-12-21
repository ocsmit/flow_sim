import numpy as np
import matplotlib.pyplot as plt
import random
from joblib import Parallel, delayed


class topo:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.array = np.zeros([self.width, self.height])
        return

    def random_index(self):

        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        return x, y

    def hill(self):

        x1, y1 = self.random_index()
        r = random.randint(10, 50)

        topo_vector = []

        # http://www.stuffwithstuff.com/robot-frog/3d/hills/hill.html
        for i in range(self.array.shape[0]):
            for j in range(self.array.shape[1]):
                z = r**2 - ((j - x1)**2 + (i - y1)**2)
                if z > 0:
                    topo_vector.append(z)
                else:
                    topo_vector.append(0)

        return topo_vector

    def generate_hills(self, number_of_hills, threads=5):
        split_range = number_of_hills // threads
        remainder = number_of_hills % threads
        split_data = [[i, i + split_range] for i in range(0,
            number_of_hills - split_range, split_range)]
        if remainder != 0:
            split_data[-1][1] += remainder
        results = []
        print(split_data)
        results = Parallel(n_jobs=threads)(delayed(self.worker)(sl) for sl in split_data)
        self.final_topo = self.array.flatten()
        for i in results:
            self.final_topo += i

    def worker(self, range_of_hills):
        vector = self.array.flatten()
        for i in range(range_of_hills[0], range_of_hills[1]):
            vector += self.hill()
        return vector

    def plot(self):
        plt.imshow(self.array)
        plt.show()







