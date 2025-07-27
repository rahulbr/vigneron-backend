const mongoose = require('mongoose');

const vineyardSchema = new mongoose.Schema({
  name: { type: String, required: true },
  location: {
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    address: String
  },
  gddBaseTemp: { type: Number, default: 50 },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Vineyard', vineyardSchema);