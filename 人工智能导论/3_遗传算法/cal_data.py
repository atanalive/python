import numpy as np

city_10 = np.array([298.83, 298.83, 307.41, 298.83, 309.42])
city_10_time = np.array([5.78, 5.74, 5.85, 6.42, 6.27])
city_20 = np.array([657, 632.4, 634.9, 642.43, 611.2])
city_20_time = np.array([7.18, 7.34, 7.72, 7.39, 6.97])
city_100 = np.array([4138.47,4260.84,4351.78,4340.35,4284.05])
city_100_time = np.array([21.89,18.47,18.32,18.94,19.48])

print(f"city_10.mean is{city_10.mean()},city_10.min is {city_10.min()}"
      f",city_10.max is {city_10.max()},city_10_time.mean is {city_10_time.mean()}")

print(f"city_20.mean is{city_20.mean()},city_20.min is {city_20.min()}"
      f",city_20.max is {city_20.max()},city_20_time.mean is {city_20_time.mean()}")
# city100仿照上面即可
print(f"city_100.mean is{city_100.mean()},city_100.min is {city_100.min()}"
      f",city_100.max is {city_100.max()},city_100_time.mean is {city_100_time.mean()}")
