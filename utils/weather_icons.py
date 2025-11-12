def get_custom_weather_icon(weather_data):
    
    weather_id = weather_data['weather'][0]['id']
    main_weather = weather_data['weather'][0]['main'].lower()
    description = weather_data['weather'][0]['description'].lower()
    
    print(f"Отладка: weather_id={weather_id}, main={main_weather}, desc={description}")
    
  
    if 200 <= weather_id <= 232:
        return 'stormy.png'
    
    
    elif 300 <= weather_id <= 321:
        return 'rainy.png'  
    
   
    elif 500 <= weather_id <= 531:
        if 'heavy' in description or 'shower' in description:
            return 'stormy.png'  
        else:
            return 'rainy.png'
    
   
    elif 600 <= weather_id <= 622:
        return 'snowy.png'
    
    
    elif 701 <= weather_id <= 781:
        return 'foggy.png'
    
    
    elif weather_id == 800:
        return 'sunny.png'
    
    
    elif 801 <= weather_id <= 804:
        if weather_id == 801:  
            return 'partly-cloudy.png'  
        else:  
            return 'cloudy.png'
    
    
    else:
        print(f"Неизвестный код погоды: {weather_id}, используется иконка по умолчанию")
        return 'default.png'