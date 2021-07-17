import pandas as pd


def main():
    data = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]

    df = pd.DataFrame(data, columns=['Site', 'Age'], dtype=float)

    print(df)


def read():
    df = pd.read_csv('./nba.csv')
    # print(df.to_string())
    # print(df.tail(2))
    print(df.head(10))


def read_json():
    jsons = '''
    [
    {
      "id": "A001",
      "name": "菜鸟教程",
      "url": "www.runoob.com",
      "likes": 61
    },
    {
      "id": "A002",
      "name": "Google",
      "url": "www.google.com",
      "likes": 124
    },
    {
      "id": "A003",
      "name": "淘宝",
      "url": "www.taobao.com",
      "likes": 45
    }
  ]
    '''


if __name__ == '__main__':
    # main()
    read()
