class Dog:
    d_type = "京巴"  # 类属性,公共属性
    __d_age = "14"  # 类属性,私有属性

    # 构造函数
    def __init__(self):
        pass
        # self.d_type = name if name != '' else ''

    # 类的方法
    def say_hello(self):
        print("Hello, my name is " + self.d_type + self.__d_age)


class Cat:
    c_type = "短尾"

    def say_hello(self):
        print(f"我是一只{self.c_type}猫")


# 实例化类
dog = Dog()
Dog.d_type = "张三"
dog.say_hello()
dog2 = Dog()
dog2.say_hello()
