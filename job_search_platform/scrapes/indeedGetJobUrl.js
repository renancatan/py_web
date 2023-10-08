const puppeteer = require('puppeteer');
const fs = require('fs');

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0 Safari/537.36',
};

async function get_data(url) {
  const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1366, height: 768 },
    });
  const page = await browser.newPage();
  await page.setExtraHTTPHeaders(headers);

  let hasNextPage = true;
  let aggregatedData = [];

  try {
    await page.goto(url);
    console.log('Status Code:', (await page.waitForResponse(response => response.status() === 200)).status());

    while (hasNextPage) {
      const jobs = await page.evaluate(() => {
        const jobElements = document.querySelectorAll('td.resultContent');
        const jobList = [];
        jobElements.forEach((element) => {
//          const jobTitle = element.querySelector('h2.jobTitle span')?.textContent;
//          const companyName = element.querySelector('span.companyName')?.textContent;
//          const companyLocation = element.querySelector('div.companyLocation')?.textContent;
          const jobLink = element.querySelector('h2.jobTitle a')?.getAttribute('href');
          jobList.push({
//            jobTitle,
//            companyName,
//            companyLocation,
            jobLink: jobLink || null
          });
        });
        return jobList;
      });

      aggregatedData = aggregatedData.concat(jobs);
      console.log(aggregatedData)
      const nextButton = await page.$('[data-testid="pagination-page-next"]');

      if (nextButton) {
        await nextButton.click();
        await page.waitForTimeout(10000);  // Waiting for 2 seconds to load the new page
      } else {
        hasNextPage = false;
      }
    }

    await browser.close();
    return aggregatedData;
  } catch (error) {
    console.error(error);
    await browser.close();
    return null;
  }
}


const indeedData = (data) => {
    fs.writeFile('./indeedLink.json', JSON.stringify(data, null, 4), (err) => {
        if (err) {
            console.error('Error writing file', err);
        } else {
            console.log('Successfully wrote to indeedData.json'); // Changed the filename here to match the actual file
        }
    });
};

async function main() {
    const url = 'https://www.indeed.com/jobs?q=python+developer&l=Remote&rbl=Remote&jlid=aaa2b906602aa8f5';
    const data = await get_data(url);
    console.log(data);
    indeedData(data);
}

main().catch(console.error);
