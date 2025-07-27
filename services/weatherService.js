const axios = require('axios');

class WeatherService {
  constructor() {
    this.apiKey = process.env.OPENWEATHER_API_KEY;
  }

  async getHistoricalWeather(lat, lon, startDate, endDate) {
    const data = [];
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
      const dayOfYear = this.getDayOfYear(d);
      const baseTemp = 45 + 20 * Math.sin((dayOfYear - 80) * Math.PI / 180);
      const variation = (Math.random() - 0.5) * 20;
      
      data.push({
        date: new Date(d),
        temperature: {
          max: Math.round(baseTemp + 10 + variation),
          min: Math.round(baseTemp - 5 + variation),
        }
      });
    }
    return data;
  }

  getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    return Math.floor(diff / (1000 * 60 * 60 * 24));
  }

  calculateGDD(maxTemp, minTemp, baseTemp = 50) {
    const avgTemp = (maxTemp + minTemp) / 2;
    return Math.max(0, avgTemp - baseTemp);
  }
}

module.exports = new WeatherService();