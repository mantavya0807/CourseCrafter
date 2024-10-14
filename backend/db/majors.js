// db.js
const mongoose = require('mongoose');

// MongoDB connection
mongoose.connect('mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('Connected to MongoDB');
}).catch((error) => {
  console.error('Error connecting to MongoDB:', error);
});

// Define schema for Majors
const majorSchema = new mongoose.Schema({
  major: String,
  degreeType: String,
  college: String
});

// Create a model for the Majors collection in the HACK database
const db = mongoose.connection.useDb('HACK');
const Major = db.model('Major', majorSchema, 'Majors');

// Export the Major model to use in other files
module.exports = { Major };
