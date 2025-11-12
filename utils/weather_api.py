import requests
from datetime import datetime
from config import Config

def get_weather_data(city_name):
   
    try:
       
        params = {
            'q': city_name,
            'appid': Config.WEATHER_API_KEY,
            'units': 'metric',  
            'lang': 'ru'        
        }
        
        print(f"Делаем запрос к API для города: {city_name}")
        
       
        response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
        
      
        if response.status_code == 200:
            
            data = response.json()
            print(f"Успешно получили данные для {data.get('name', 'Unknown')}")
            
           
            processed_data = process_weather_data(data)
            return processed_data, None
            
        elif response.status_code == 404:
            
            error_msg = f"Город '{city_name}' не найден. Проверьте правильность написания."
            print(f"Ошибка: {error_msg}")
            return None, error_msg
            
        else:
            error_msg = f"Ошибка API: {response.status_code} - {response.text}"
            print(f"Ошибка: {error_msg}")
            return None, error_msg
            
    except requests.exceptions.Timeout:
        error_msg = "Таймаут запроса. Сервер погоды не отвечает. Попробуйте позже."
        print(f"Ошибка: {error_msg}")
        return None, error_msg
        
    except requests.exceptions.ConnectionError:
        error_msg = "Ошибка соединения. Проверьте интернет-подключение."
        print(f"Ошибка: {error_msg}")
        return None, error_msg
        
    except Exception as e:
        error_msg = f"Неизвестная ошибка: {str(e)}"
        print(f"Ошибка: {error_msg}")
        return None, error_msg


def process_weather_data(raw_data):
   
    weather_info = {
        'city': raw_data.get('name', 'Неизвестно'),
        'country': raw_data.get('sys', {}).get('country', ''),
        'temperature': round(raw_data['main']['temp']),
        'feels_like': round(raw_data['main']['feels_like']),
        'description': raw_data['weather'][0]['description'],
        'humidity': raw_data['main']['humidity'],
        'pressure': raw_data['main']['pressure'],
        'wind_speed': raw_data['wind']['speed'],
        'weather_id': raw_data['weather'][0]['id'],  
        'main_weather': raw_data['weather'][0]['main'],  
        'timestamp': datetime.now().strftime('%H:%M %d.%m.%Y')
    }
    
    
    print(f"Обработанные данные: {weather_info['city']}, {weather_info['temperature']}°C")
    return weather_info