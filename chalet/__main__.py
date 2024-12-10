from reading import __reading__ as rd


def main():
    print("Chalet is running")
    temp = rd.get_current_temperature()
    weather = rd.current_weather_condition()
    print("Weather: ", weather)
    

if __name__ == '__main__':
    main()