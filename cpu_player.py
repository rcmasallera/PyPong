import pandas


def read_data():
    pong_data = pandas.read_csv("play.csv")
    pong_data.drop_duplicates()

    return pong_data
