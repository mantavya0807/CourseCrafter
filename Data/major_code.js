const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// Array of major codes
const majorCodes = [
  "ACCTG", "ACS", "ADTED", "AERSP", "AFAM", "AFR", "AGBM", "ABSM", "AEE", "AGCOM",
  "AGSC", "ASM", "AG", "AGECO", "AGRO", "AIR", "AMST", "ANSC", "ANTH", "ABA",
  "APLNG", "AYFCE", "ARAB", "AE", "AET", "ARCH", "ARMY", "ART", "AED", "ARTH",
  "A-I", "ARTSA", "AA", "AAS", "ASIA", "ASTRO", "ATHTR", "BESC", "BBH", "BMB",
  "BIOET", "BMH", "BE", "BISC", "BIOL", "BME", "BE_T", "BRS", "BIOTC", "BA",
  "BLAW", "CHE", "CHEM", "CMAS", "CHNS", "CIVCM", "CE", "CET", "CAMS", "CAS",
  "CSD", "COMM", "CEDEV", "CED", "CIED", "CMLIT", "CMPMT", "CMPEH", "CMPEN",
  "CMPET", "CMPSC", "CC", "CNED", "CRIMJ", "CRIM", "CI", "C-S", "CYBER",
  "DANCE", "DA", "DS", "DART", "DIGIT", "DMD", "ECE", "EMSC", "EARTH", "ECON",
  "EDUC", "EDMTH", "EDLDR", "EDPSY", "EDTEC", "EDTHP", "EE", "EET", "EMET",
  "ELEDM", "EGEE", "EME", "EBF", "ENNEC", "ENGR", "EDSGN", "EGT", "EMCH",
  "ESC", "ET", "ENGL", "ESL", "ETI", "ENT", "ENTR", "ENVE", "ERM", "ENVSC",
  "ENVST", "ENVSE", "FIN", "FINSV", "CAP", "FDSC", "FDSYS", "FRNAR", "FRNSC",
  "FORT", "FOR", "FR", "FSC", "GAME", "GEOG", "GEOSC", "GER", "GLIS", "GD",
  "GREEK", "HHD", "HLHED", "HHUM", "HPA", "HEBR", "HIED", "HINDI", "HIST",
  "HLS", "HONOR", "HORT", "HM", "HDFS", "HRM", "HCDD", "HUM", "HSS", "IE",
  "IET", "IST", "ITECH", "INSYS", "INART", "ISB", "INTAG", "IB", "INTST",
  "INTSP", "IT", "JAPNS", "JST", "KINES", "KOR", "LER", "LHR", "LARCH",
  "LLED", "Less Commonly Taught", "LATIN", "LATAM", "LTNST", "LPE", "LDT",
  "LA", "LST", "LING", "MGMT", "MIS", "MKTG", "MAET", "MATSE", "MATH",
  "MTHED", "ME", "MET", "MEDVL", "METEO", "MICRB", "MNPR", "MNG", "MNGT",
  "MUSIC", "BRASS", "JAZZ", "KEYBD", "PERCN", "STRNG", "VOICE", "WWNDS",
  "NAVSC", "NUCE", "NURS", "NUTR", "OS", "OT", "OLEAD", "PNG", "PHIL",
  "PHOTO", "PT", "PHYS", "PLANT", "PPEM", "PLET", "POL", "PLSC", "PES",
  "PORT", "PSU", "PSYCH", "PHP", "PUBPL", "PPOL", "QMM", "QC", "RADSC",
  "RTE", "RPTM", "RHS", "RLST", "RM", "RSOC", "RUS", "SSET", "SPSY",
  "SC", "SCIED", "STS", "SRA", "SLAV", "SODA", "SSED", "SOCW", "SOC",
  "SWENG", "SOILS", "SPAN", "SPLED", "STAT", "SCM", "SUR", "SUST", "SWA",
  "EDAB", "THEA", "TURF", "UKR", "VBSC", "WILDL", "WFS", "WGSS", "WMNST",
  "WP", "WFED", "WLED"
];

// Base URL
const baseURL = 'https://bulletins.psu.edu/university-course-descriptions/undergraduate/';

// Function to convert major code to lowercase (handle special cases)
function convertToURLCode(code) {
    // Replace any special characters if needed, e.g., "A-I" to "a-i"
    return code.toLowerCase();
}

// Function to scrape cross-listed courses for a given major code
async function scrapeMajorCourses(majorCode) {
    const url = `${baseURL}${convertToURLCode(majorCode)}/`;
    console.log(`Scraping Major: ${majorCode} | URL: ${url}`);

    try {
        const { data } = await axios.get(url);
        const $ = cheerio.load(data);

        const courses = [];

        // Select all course blocks
        $('div.courseblockmeta.active').each((index, element) => {
            const courseBlock = $(element);

            // Extract Course Code and Name
            const courseDesc = courseBlock.find('div.courseblockdesc p').first().text().trim();
            console.log(courseDesc);
            const courseNameMatch = courseDesc.match(/([A-Z\-]+)\s+(\d+)\s+(.+?)\s+\(\d+\)/);

            let courseCode = '';
            let courseName = '';

            if (courseNameMatch) {
                courseCode = `${courseNameMatch[1]} ${courseNameMatch[2]}`;
                courseName = courseNameMatch[3];
            } else {
                // Alternative parsing if the above regex doesn't match
                const link = courseBlock.find('div.courseblockdesc p a.bubblelink.code');
                if (link.length) {
                    const codeText = link.text().replace(/\u00A0/g, ' ').trim(); // Replace non-breaking space
                    courseCode = codeText;
                    courseName = courseBlock.find('div.courseblockdesc p').text().split(codeText)[0].trim();
                }
            }

            // Extract Cross-Listed Courses
            let crossListed = [];
            const extraInfo = courseBlock.find('div.courseblockextra p.noindent');

            if (extraInfo.length) {
                // Assuming cross-listed courses are mentioned here
                extraInfo.find('a.bubblelink.code').each((i, el) => {
                    const crossCode = $(el).text().replace(/\u00A0/g, ' ').trim();
                    crossListed.push(crossCode);
                });
            }

            courses.push({
                major: majorCode,
                courseCode: courseCode,
                courseName: courseName,
                crossListed: crossListed
            });
        });

        return courses;

    } catch (error) {
        console.error(`Error scraping major ${majorCode}:`, error.message);
        return [];
    }
}

// Main function to iterate through all major codes and scrape data
async function scrapeAllMajors() {
    const allCourses = [];

    for (const major of majorCodes) {
        const majorCourses = await scrapeMajorCourses(major);
        allCourses.push(...majorCourses);
    }

    // Save the data to a JSON file
    const outputPath = path.join(__dirname, 'allMajorCourses.json');
    fs.writeFileSync(outputPath, JSON.stringify(allCourses, null, 2));
    console.log(`Scraping completed. Data saved to ${outputPath}`);
}

// Execute the scraper
scrapeAllMajors();
