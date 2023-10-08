const fs = require('fs');


fs.readFile('./indeedData.json', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file', err);
  } else {
    const jsonData = JSON.parse(data);
    const jobsUrl = jsonData.map( (urls) => urls.jobLink.replace("/rc/clk", "https://www.indeed.com/viewjob") )
    console.log(jobsUrl);

  }
});
