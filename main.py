import pandas as pd
import uberx

data = pd.read_csv('Uber Data/Rider/trips_data.csv')

if __name__ == '__main__':
    uberx.uber_x(data)
