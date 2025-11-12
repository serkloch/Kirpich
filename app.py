from flask import Flask, render_template, request, flash, jsonify
from config import Config
from utils.weather_api import get_weather_data
from utils.weather_icons import get_custom_weather_icon


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    print("Загружена главная страница")
    return render_template('index.html',
                         default_city=app.config['DEFAULT_CITY'])

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
    else:
        city = request.args.get('city', app.config['DEFAULT_CITY'])
    
   
    if not city:
        city = app.config['DEFAULT_CITY']
    
    print(f"Запрос погоды для города: {city}")
    
  
    weather_data, error = get_weather_data(city)
    
    if error:
        flash(error, 'error')
        return render_template('weather.html',
                             weather=None,
                             searched_city=city)
    
    if weather_data:
        custom_icon = get_custom_weather_icon({
            'weather': [{
                'id': weather_data['weather_id'],
                'main': weather_data['main_weather'],
                'description': weather_data['description']
            }]
        })
        
        
        weather_data['custom_icon'] = f"weather/{custom_icon}"
        
        print(f"Используется иконка: {custom_icon} для погоды: {weather_data['description']}")
    
    
    return render_template('weather.html',
                         weather=weather_data,
                         searched_city=city)

@app.route('/api/weather/<city>')
def api_weather(city):
    weather_data, error = get_weather_data(city)
    custom_icon = get_custom_weather_icon({
        'weather': [{
            'id': weather_data['weather_id'],
            'main': weather_data['main_weather'],
            'description': weather_data['description']
        }]
    })
    
    weather_data['custom_icon'] = f"weather/{custom_icon}"
    return jsonify(weather_data)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("Запуск Flask приложения...")
    print(f"Доступно по адресу: http://localhost:5000")
    app.run(debug=app.config.get('DEBUG', True))