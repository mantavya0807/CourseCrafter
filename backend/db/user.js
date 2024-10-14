const mongoose = require('mongoose');

// MongoDB connection (adjust your MongoDB URI here if needed)
mongoose.connect('mongodb+srv://Aayush9930:Aayush%409930@cluster0.vqsor.mongodb.net/HACK', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => {
  console.log('Connected to MongoDB');
}).catch((err) => {
  console.error('Error connecting to MongoDB:', err);
});

// User Schema
const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

// User Model
const User = mongoose.model('User', userSchema);

module.exports = User;
