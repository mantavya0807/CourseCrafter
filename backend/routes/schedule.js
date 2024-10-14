const express = require('express');
const EventEmitter = require('events');
const router = express.Router();
const scheduleEmitter = new EventEmitter();
const {
  getMajorCourses,
  getMinorCourses,
  getCertificateCourses,
  getGenEdCourses,
  buildPrerequisiteGraph,
  topologicalSort,
  assignCoursesToSemesters
} = require('../utils/scheduler');

function removeDuplicates(courses) {
  const uniqueCourses = [];
  const courseSet = new Set();

  for (const course of courses) {
    if (!courseSet.has(course.code)) {
      courseSet.add(course.code);
      uniqueCourses.push(course);
    }
  }
  return uniqueCourses;
}

router.post('/', async (req, res) => {
  const { majors, minors = [], certificates = [], targetSemesters } = req.body;

  if (!majors || !Array.isArray(majors) || majors.length === 0 || !targetSemesters || targetSemesters < 2) {
    return res.status(400).json({ success: false, message: 'Invalid input: majors and targetSemesters are required' });
  }

  try {
    console.log('Fetching courses...');

    // Fetch courses for each major, minor, and certificate
    const majorCourses = await Promise.all(majors.map(major => getMajorCourses(major)));
    const minorCourses = await Promise.all(minors.map(minor => getMinorCourses(minor)));
    const certificateCourses = await Promise.all(certificates.map(cert => getCertificateCourses(cert)));
    const genEdCourses = getGenEdCourses();

    // Combine all fetched courses
    let allCourses = [...majorCourses.flat(), ...minorCourses.flat(), ...certificateCourses.flat(), ...genEdCourses];

    // Remove duplicates from the course list
    allCourses = removeDuplicates(allCourses);

    // Build prerequisite graph and perform topological sorting
    const { graph, inDegree } = buildPrerequisiteGraph(allCourses);
    const sortedCourses = topologicalSort(graph, inDegree);

    // Create a course map for easy access by course code
    const courseMap = {};
    allCourses.forEach(course => {
      courseMap[course.code] = course;
    });

    // Assign courses to semesters
    let schedule = assignCoursesToSemesters(sortedCourses, courseMap, targetSemesters);

    // If no schedule could be generated, return an error
    if (!schedule || schedule.length === 0) {
      return res.status(400).json({ success: false, message: 'Unable to generate a valid schedule with the given inputs' });
    }

    // Send the final schedule back as the response
    res.status(200).json({ success: true, data: { schedule } });
  } catch (error) {
    console.error('Error generating schedule:', error);
    res.status(500).json({ success: false, message: 'An internal server error occurred', error: error.message });
  }
});

module.exports = { router, scheduleEmitter };
