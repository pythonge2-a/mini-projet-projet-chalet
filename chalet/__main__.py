from reading import __reading__ as rd

def main():
    print("Chalet is running")
    temp = rd.get_current_temperature()
    weather = rd.get_current_weather_condition()
    rd.show_all_graphs()
    print("Current temperature is: ", temp)
    print("Current weather is: ", weather)
    

if __name__ == '__main__':
    main()