const mongoose = require('mongoose');

function getRandomElement(array) {
  return array[Math.floor(Math.random() * array.length)];
}
// Fetch courses for a selected major from the MajorPath database
async function getMajorCourses(majorName) {
    let majorDb = mongoose.connection.useDb('MajorPath');
    const formattedMajorName = majorName.replace(/\s+/g, '_');
    let collectionName = `${formattedMajorName}_B.S._collection`;
  
    try {
      let majorCourses = await majorDb.collection(collectionName).find({}).toArray();
  
      const hackDb = mongoose.connection.useDb('HACK');
      const coursePromises = majorCourses.map(async (majorCourse) => {
        const courseCodes = majorCourse.course_code.split('|').map(code => code.trim());
        const selectedCourseCode = getRandomElement(courseCodes);
        const courseDetails = await hackDb.collection('Courses').findOne({ coursename: selectedCourseCode });
        console.log(courseDetails);
        return {
          code: selectedCourseCode,
          title: courseDetails?.title || 'Unknown Title',
          credits: majorCourses.credits || 3,
          prerequisites: courseDetails?.prerequisite || [],
          mandatory: majorCourse.Mandatory === 1
        };
      });
  
      return Promise.all(coursePromises);
    } catch (error) {
      console.error(`Error fetching major courses for ${majorName}:`, error);
      throw new Error(`Could not fetch major courses for ${majorName}`);
    }
  }
async function getMinorCourses(minorName) {
  try {
    let minorDb = mongoose.connection.useDb('MinorPath');
    const formattedMinorName = minorName.replace(/\s+/g, '_');
    let collectionName = `${formattedMinorName}`;
    
    const minorCourses = await minorDb.collection(collectionName).find({ minor: minorName }).toArray();

    const hackDb = mongoose.connection.useDb('HACK');
    const coursePromises = minorCourses.map(async (minorCourse) => {
      const courseCodes = minorCourse.course_code.split('|').map(code => code.trim());
      const selectedCourseCode = getRandomElement(courseCodes);
      const courseDetails = await hackDb.collection('Courses').findOne({ coursename: selectedCourseCode });
      console.log(courseDetails);
      return {
        code: course.Course_Code,
        title: courseDetails?.title || 'Unknown Title',
        credits: course.Credits || 3,
        prerequisites: courseDetails?.prerequisite || []
      };
    });

    return Promise.all(coursePromises);
  } catch (error) {
    console.error(`Error fetching minor courses for ${minorName}:`, error);
    throw new Error(`Could not fetch minor courses for ${minorName}`);
  }
}

async function getCertificateCourses(certificateName) {
  try {
    const certificateDb = mongoose.connection.useDb('CertificatePath');
    const formattedcertificateName = certificateName.replace(/\s+/g, '_');
    let collectionName = `${formattedcertificateName}`;
    const certificateCourses = await certificateDb.collection(collectionName).find({ Certificate: certificateName }).toArray();

    const hackDb = mongoose.connection.useDb('HACK');
    const coursePromises =certificateCourses.map(async (certificateCourse) => {
      const courseCodes = certificateCourse.course_code.split('|').map(code => code.trim());
      const selectedCourseCode = getRandomElement(courseCodes);
      const courseDetails = await hackDb.collection('Courses').findOne({ coursename: selectedCourseCode });
      console.log(courseDetails);
      return {
        code: course.Course_Code,
        title: courseDetails?.title || 'Unknown Title',
        credits: course.Credits || 3,
        prerequisites: courseDetails?.prerequisite || []
      };
    });

    return Promise.all(coursePromises);
  } catch (error) {
    console.error(`Error fetching certificate courses for ${certificateName}:`, error);
    throw new Error(`Could not fetch certificate courses for ${certificateName}`);
  }
}

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
function cleanPrerequisite(prereq) {
  return prereq.replace(/\xa0/g, ' ').trim();
}

function parsePrerequisites(prerequisites) {
  if (Array.isArray(prerequisites)) {
    return prerequisites;
  } else if (typeof prerequisites === 'string') {
    try {
      return JSON.parse(prerequisites.replace(/'/g, '"'));
    } catch (error) {
      console.warn(`Failed to parse prerequisites: ${prerequisites}`);
      return [];
    }
  }
  return [];
}

function getGenEdCourses() {
  const genEdCourses = [
    { code: "GH_1", title: "General Humanities 1", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GH_2", title: "General Humanities 2", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GW_1", title: "General Writing 1", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GW_2", title: "General Writing 2", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GN_1", title: "General Natural Sciences 1", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GN_2", title: "General Natural Sciences 2", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GS_1", title: "General Social Sciences 1", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GA_1", title: "General Arts 1", credits: 3, prerequisites: [], mandatory: "true" },
    { code: "GA_2", title: "General Arts 2", credits: 3, prerequisites: [], mandatory: "true" }
  ];
  return genEdCourses;
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function buildPrerequisiteGraph(courses) {
  const graph = {};
  const inDegree = {};

  courses.forEach(course => {
    graph[course.code] = [];
    inDegree[course.code] = 0;
  });

  courses.forEach(course => {
    if (Array.isArray(course.prerequisites)) {
      course.prerequisites.forEach(prereq => {
        if (graph[prereq]) {
          graph[prereq].push(course.code);
          inDegree[course.code]++;
        } else {
          console.warn(`Prerequisite ${prereq} for course ${course.code} not found in the course list.`);
        }
      });
    } else if (typeof course.prerequisites === 'string') {
      try {
        const prereqs = JSON.parse(course.prerequisites.replace(/'/g, '"'));
        prereqs.forEach(prereq => {
          if (graph[prereq]) {
            graph[prereq].push(course.code);
            inDegree[course.code]++;
          } else {
            console.warn(`Prerequisite ${prereq} for course ${course.code} not found in the course list.`);
          }
        });
      } catch (error) {
        console.warn(`Invalid prerequisite format for ${course.code}: ${course.prerequisites}`);
      }
    }
  });

  return { graph, inDegree };
}

function topologicalSort(graph, inDegree) {
  const sorted = [];
  const queue = Object.keys(inDegree).filter(course => inDegree[course] === 0);

  while (queue.length > 0) {
    const course = queue.shift();
    sorted.push(course);

    graph[course].forEach(dependent => {
      inDegree[dependent]--;
      if (inDegree[dependent] === 0) {
        queue.push(dependent);
      }
    });
  }

  if (sorted.length !== Object.keys(graph).length) {
    console.warn('Some courses could not be sorted due to cyclic dependencies or missing prerequisite data.');
  }

  return sorted;
}

function assignCoursesToSemesters(sortedCourses, courseMap, targetSemesters) {
  console.log(`Assigning ${sortedCourses.length} courses to ${targetSemesters} semesters`);

  const schedule = Array.from({ length: targetSemesters }, () => ({
    courses: [],
    totalCredits: 0
  }));

  const completed = new Set();
  const unassignedCourses = [];
  const genEdCourses = sortedCourses.filter(code => courseMap[code].category);
  const majorCourses = sortedCourses.filter(code => !courseMap[code].category);

  function canAssignCourse(course, semester) {
    const prereqs = parsePrerequisites(course.prerequisites);
    const prereqsMet = prereqs.every(prereq => completed.has(prereq));
    const creditsInRange = schedule[semester].totalCredits + course.credits <= 18;
    return prereqsMet && creditsInRange;
  }

  function assignCourse(courseCode, semester) {
    const course = courseMap[courseCode];
    if (!course) {
      console.warn(`Course ${courseCode} not found in courseMap.`);
      return false;
    }

    if (canAssignCourse(course, semester)) {
      schedule[semester].courses.push(course);
      schedule[semester].totalCredits += course.credits;
      completed.add(courseCode);
      console.log(`Assigned ${courseCode} to semester ${semester + 1}`);
      return true;
    }
    return false;
  }

  // Distribute Gen-Ed courses
  for (let semester = 0; semester < targetSemesters; semester++) {
    if (genEdCourses.length > 0) {
      const genEdCourse = genEdCourses.shift();
      assignCourse(genEdCourse, semester);
    }
  }

  // Assign major courses respecting prerequisites
  for (const courseCode of majorCourses) {
    let assigned = false;
    for (let semester = 0; semester < targetSemesters; semester++) {
      if (assignCourse(courseCode, semester)) {
        assigned = true;
        break;
      }
    }
    if (!assigned) {
      unassignedCourses.push(courseCode);
    }
  }

  // Assign remaining Gen-Ed courses
  while (genEdCourses.length > 0) {
    const genEdCourse = genEdCourses.shift();
    let assigned = false;
    for (let semester = 0; semester < targetSemesters; semester++) {
      if (assignCourse(genEdCourse, semester)) {
        assigned = true;
        break;
      }
    }
    if (!assigned) {
      unassignedCourses.push(genEdCourse);
    }
  }

  if (unassignedCourses.length > 0) {
    console.warn(`The following courses could not be assigned: ${unassignedCourses.join(', ')}`);
  }

  console.log('Final schedule:', JSON.stringify(schedule, null, 2));
  return schedule;
}

module.exports = {
  getMajorCourses,
  getMinorCourses,
  getCertificateCourses,
  getGenEdCourses,
  buildPrerequisiteGraph,
  topologicalSort,
  assignCoursesToSemesters
};