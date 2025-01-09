from sonic import *

if __name__ == "__main__":
    sonictest = SonicCar()

    try:
        x = sonictest.get_sonic()
        print(x)
    except:
        print("fail")
