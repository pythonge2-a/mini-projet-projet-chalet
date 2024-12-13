from reading import __reading__ as rd


def main():
    print("Chalet is running")
    temp = rd.get_current_temperature()
    print("Current temperature is: ", temp)
    

if __name__ == '__main__':
    main()