const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors({
  origin: ['http://localhost:3000', 'http://localhost:5173']
}));
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/vigneron-ai')
  .then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.error('❌ MongoDB connection error:', err));

// Routes - Add detailed error handling
console.log('📂 Loading API routes...');
try {
  const apiRoutes = require('./routes/api');
  app.use('/api', apiRoutes);
  console.log('✅ API routes loaded successfully');
} catch (error) {
  console.error('❌ Error loading API routes:', error.message);
  console.error('❌ Stack trace:', error.stack);
}

// Test route
app.get('/api/test', (req, res) => {
  res.json({ message: 'API is working!' });
});

// Debug: List all loaded routes
app.get('/api/debug/routes', (req, res) => {
  const routes = [];
  app._router.stack.forEach(function(r){
    if (r.route && r.route.path){
      routes.push(r.route.path);
    }
  });
  res.json({ routes: routes });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'Server is running!', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
