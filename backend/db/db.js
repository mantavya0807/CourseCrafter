const mongoose = require('mongoose');

// Hardcoded MongoDB connection string (replace with your actual MongoDB URI)
const mongoURI = 'mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/';

const connectToDB = async () => {
  try {
    await mongoose.connect(mongoURI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('Connected to MongoDB');
    return mongoose.connection.db;
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
    throw new Error('Could not connect to MongoDB');
  }
};

module.exports = connectToDB;
