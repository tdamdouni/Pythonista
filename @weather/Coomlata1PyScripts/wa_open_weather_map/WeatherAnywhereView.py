import ui, WeatherAnywhere as wa

#@ui.in_background
def get_weather():
  city = id = ''
  lat, lon = wa.get_current_lat_lon()
  # Call api from www.openweathermap.org
  w,f = wa.get_weather_dicts(lat,lon,city,id)
  w = wa.get_current_weather(w)
  f = wa.get_forecast(f)
  fmt = '{}\n{}\nWeather information provided by openweathermap.org'
  return fmt.format(w, f)

weather_text = get_weather()

class WeatherAnywhereView(ui.View):
    def __init__(self):
        self.hidden = True
        self.present()
        self.add_subview(ui.TextView(name='TextView', frame=self.bounds))
        self['TextView'].text = weather_text
        self.hidden = False

WeatherAnywhereView()
