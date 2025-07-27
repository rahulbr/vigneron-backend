const express = require('express');
const router = express.Router();
const Vineyard = require('../models/Vineyard');
const weatherService = require('../services/weatherService');

// Create vineyard
router.post('/vineyards', async (req, res) => {
  try {
    const vineyard = new Vineyard(req.body);
    await vineyard.save();
    res.status(201).json(vineyard);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Get all vineyards
router.get('/vineyards', async (req, res) => {
  try {
    const vineyards = await Vineyard.find({});
    res.json(vineyards);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get vineyard
router.get('/vineyards/:id', async (req, res) => {
  try {
    const vineyard = await Vineyard.findById(req.params.id);
    if (!vineyard) {
      return res.status(404).json({ error: 'Vineyard not found' });
    }
    res.json(vineyard);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get GDD data for vineyard
router.get('/vineyards/:id/gdd', async (req, res) => {
  try {
    const vineyard = await Vineyard.findById(req.params.id);
    if (!vineyard) {
      return res.status(404).json({ error: 'Vineyard not found' });
    }

    const year = req.query.year || new Date().getFullYear();
    const startDate = `${year}-03-01`;
    const endDate = `${year}-11-30`;

    const weatherData = await weatherService.getHistoricalWeather(
      vineyard.location.latitude,
      vineyard.location.longitude,
      startDate,
      endDate
    );

    let cumulativeGDD = 0;
    const gddData = weatherData.map(day => {
      const dailyGDD = weatherService.calculateGDD(
        day.temperature.max,
        day.temperature.min,
        vineyard.gddBaseTemp
      );
      cumulativeGDD += dailyGDD;
      
      return {
        date: day.date.toISOString().split('T')[0],
        dateFormatted: day.date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        dailyGDD: Math.round(dailyGDD * 10) / 10,
        cumulativeGDD: Math.round(cumulativeGDD),
        maxTemp: day.temperature.max,
        minTemp: day.temperature.min
      };
    });

    res.json({
      vineyard: {
        name: vineyard.name,
        location: vineyard.location
      },
      gddData,
      totalGDD: cumulativeGDD,
      year: parseInt(year)
    });

  } catch (error) {
    console.error('GDD calculation error:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;