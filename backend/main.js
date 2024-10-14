const express = require('express');
const mongoose = require('mongoose');
const User = require('./db/user'); // Importing the User model from user.js
const { Major } = require('./db/majors');
const { router: scheduleRouter, scheduleEmitter } = require('./routes/schedule');
const app = express();
const schedule = require('./routes/schedule');

const port = 3000;
const cors = require('cors');
app.use(express.json());
app.use(cors());
const rearrangedSchedule = require('./utils/scheduler');
app.use('/schedule', scheduleRouter);

// Listen for the rearranged schedule
scheduleEmitter.on('scheduleRearranged', (rearrangedSchedule) => {
  console.log('Rearranged schedule received in main.js:', rearrangedSchedule);
  // You can now use the rearrangedSchedule in your main.js file
});

// Signup Route
app.post('/signup', async (req, res) => {
  const { email, password, name } = req.body;

  try {
    // Check if the user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).send('User already exists');
    }

    // Create and save the new user
    const newUser = new User({ email, password, name });
    await newUser.save();

    return res.status(200).send('Signup Successful');
  } catch (err) {
    console.error('Error during signup:', err);
    return res.status(500).send('Internal Server Error');
  }
});

// Login Route
app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    // Check if the user exists with the provided email and password
    const user = await User.findOne({ email, password });
    if (user) {
      return res.status(200).send('Login Successful');
    } else {
      return res.status(401).send('Unauthorized');
    }
  } catch (err) {
    return res.status(500).send('Internal Server Error');
  }
});

// Majors Route
app.get('/majors', async (req, res) => {
  try {
    // Access the HACK database
    const db = mongoose.connection.useDb('HACK'); // Use the 'HACK' database

    // Fetch the list of majors
    const majorsList = await db.collection('Majors').find({}, { projection: { Major: 1, _id: 0 } }).toArray();
    // Return an array of major names
    const majors = majorsList.map(major => major.Major);

    return res.status(200).json(majors);
  } catch (error) {
    console.error('Error retrieving majors:', error);
    return res.status(500).json({ message: 'Error retrieving majors', error: error.message });
  }
});

// Minors Route
app.get('/minors', async (req, res) => {
  try {
    // Access the HACK database
    const db = mongoose.connection.useDb('HACK'); // Use the 'HACK' database

    // Fetch the list of minors
    const minorsList = await db.collection('Minors').find({}, { projection: { Minor: 1, _id: 0 } }).toArray();
    // Return an array of minor names
    const minors = minorsList.map(minor => minor.Minor);

    return res.status(200).json(minors);
  } catch (error) {
    console.error('Error retrieving minors:', error);
    return res.status(500).json({ message: 'Error retrieving minors', error: error.message });
  }
});

// Certificates Route
app.get('/certificates', async (req, res) => {
  try {
    const db = mongoose.connection.useDb('HACK'); // Use the 'HACK' database
    const certificatesList = await db.collection('Certificates').find({}, { projection: { Certificate: 1, _id: 0 } }).toArray();
    const certificates = certificatesList.map(cert => cert.Certificate);
    return res.status(200).json(certificates);
  } catch (error) {
    console.error('Error retrieving certificates:', error);
    return res.status(500).json({ message: 'Error retrieving certificates', error: error.message });
  }
});

// Classes Route
app.get('/classes', async (req, res) => {
  try {
    const db = mongoose.connection.useDb('HACK'); // Use the 'HACK' database
    const classesList = await db.collection('Courses').find({}, { projection: { coursename: 1, _id: 0 } }).toArray();
    const classes = classesList.map(cls => cls.coursename);
    return res.status(200).json(classes);
  } catch (error) {
    console.error('Error retrieving classes:', error);
    return res.status(500).json({ message: 'Error retrieving classes', error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
