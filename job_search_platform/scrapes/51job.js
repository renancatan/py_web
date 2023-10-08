const puppeteer = require('puppeteer');
const fs = require('fs');

//async function run() {
//    const browser = await puppeteer.launch({
//        headless: true,
//        defaultViewport: { width: 1366, height: 768 },
//    });
//
//    const page = await browser.newPage();
//
//    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3");
//
//    await page.goto("https://we.51job.com/pc/search?keyword=python%20developer&searchType=2&sortType=0&metro=");
//
//    await page.waitForTimeout(7000);  // 10000 works
//
//    await page.waitForSelector('.j_joblist');
//
//    await page.mouse.move(100, 100);
//    await page.mouse.move(200, 200);
//
//    const jobsData = await page.evaluate(() => {
//        let jobs = Array.from(document.querySelectorAll('.j_joblist'));
//        return jobs.map(job => {
//            let titles = Array.from(job.querySelectorAll('.jname.at')).map(titleElement => titleElement.innerText);
//            let salaries = Array.from(job.querySelectorAll('.sal')).map(salaryElement => salaryElement.innerText);
//
//            const combined = titles.map((title, index) => ({
//                title,
//                salary: salaries[index] || 'N/A' // Use 'N/A' if salary data for this title is not available
//            }));
//
//            return {
//                data: job.innerHTML,
////                combined
//            };
//        });
//    });
//
//    console.log(jobsData);
//
//
//
//    // Save as JSON
//    fs.writeFile('jobsData.json', JSON.stringify(jobsData, null, 4), (err) => {
//        if (err) {
//            console.error('Error writing file', err);
//        } else {
//            console.log('Successfully wrote to jobsData.json');
//        }
//    });
//
//    await browser.close();
//}
//
//run();



// COMPLETE CODE BELOW

async function run() {
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1366, height: 768 },
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3");

    await page.goto("https://we.51job.com/pc/search?keyword=python%20developer&searchType=2&sortType=0&metro=");
    await page.waitForTimeout(15000);
    await page.waitForSelector('.j_joblist', { timeout: 10000 });

    let allJobsData = [];

    const classNames = [
    'e_icons.ick',
    'el',
    't',
    'jname.at',
    'chat',
    'chat-img',
    'info',
    'sal',
    'd.at',
    'tags',
    'er',
    'cname.at',
    'dc.at',
    'int.at',
    'p_but'
    ];
    while (true) {
//    let pageCount = 0;
//    while (pageCount < 2) {
        const jobsData = await page.evaluate(() => {
            let jobs = Array.from(document.querySelectorAll('.j_joblist'));
            return jobs.map(job => {

                let icons = Array.from(job.querySelectorAll('.e_icons.ick')).map(titleElement => titleElement.innerText);
                let el = Array.from(job.querySelectorAll('.el')).map(salaryElement => salaryElement.innerText);
                let t = Array.from(job.querySelectorAll('.t')).map(titleElement => titleElement.innerText);
                let titles = Array.from(job.querySelectorAll('.jname.at')).map(titleElement => titleElement.innerText);
                let chat = Array.from(job.querySelectorAll('.chat')).map(salaryElement => salaryElement.innerText);
                let chatImg = Array.from(job.querySelectorAll('.chat-img')).map(titleElement => titleElement.innerText);
                let info = Array.from(job.querySelectorAll('.info')).map(salaryElement => salaryElement.innerText);
                let salaries = Array.from(job.querySelectorAll('.sal')).map(salaryElement => salaryElement.innerText);
                let dAt = Array.from(job.querySelectorAll('.d.at')).map(titleElement => titleElement.innerText);
                let tags = Array.from(job.querySelectorAll('.tags')).map(salaryElement => salaryElement.innerText);
                let er = Array.from(job.querySelectorAll('.er')).map(salaryElement => salaryElement.innerText);
                let companies = Array.from(job.querySelectorAll('.cname.at')).map(titleElement => titleElement.innerText);
                let dcAt = Array.from(job.querySelectorAll('.dc.at')).map(salaryElement => salaryElement.innerText);
                let intAt = Array.from(job.querySelectorAll('.int.at')).map(titleElement => titleElement.innerText);
                let pBut = Array.from(job.querySelectorAll('.p_but')).map(salaryElement => salaryElement.innerText);


                return titles.map((title, index) => ({
                    icons: icons[index] || 'N/A',
                    el: el[index] || 'N/A',
                    t: t[index] || 'N/A',
                    title,
                    chat: chat[index] || 'N/A',
                    chatImg: chatImg[index] || 'N/A',
                    info: info[index] || 'N/A',
                    salaries: salaries[index] || 'N/A',
                    dAt: dAt[index] || 'N/A',
                    tags: tags[index] || 'N/A',
                    er: er[index] || 'N/A',
                    companies: companies[index] || 'N/A',
                    dcAt: dcAt[index] || 'N/A',
                    intAt: intAt[index] || 'N/A',
                    pBut: pBut[index] || 'N/A',
                }));
            }).flat();
        });

        allJobsData = [...allJobsData, ...jobsData];
        console.log(`Jobs on current page: ${jobsData.length}`);
        console.log(`Total jobs so far: ${allJobsData.length}`);

//        pageCount++;

        // Get the last page number
        const lastPageNumber = await page.evaluate(() => {
            const pageNumbers = Array.from(document.querySelectorAll('.el-pager .number')).map(el => +el.innerText);
            return Math.max(...pageNumbers);
        });
        console.log(`Last page: ${lastPageNumber}`);
        // Get the current page number
        const currentPageNumber = await page.evaluate(() => {
            const activePageElement = document.querySelector('.el-pager .number.active');
            return activePageElement ? +activePageElement.innerText : 1;
        });
        console.log(`Current page: ${currentPageNumber}`);
        // Break the loop if you are on the last page
        if (currentPageNumber >= lastPageNumber) break;

        // Go to the next page
        const nextPageButton = await page.$('.el-icon-arrow-right');
        if (nextPageButton) {
            await nextPageButton.click();
            await page.waitForTimeout(5000);
            await page.waitForSelector('.j_joblist');
        } else {
            break;
        }
    }

    // Save as JSON
    fs.writeFile('./scrapes/jobsData.json', JSON.stringify(allJobsData, null, 4), (err) => {
        if (err) {
            console.error('Error writing file', err);
        } else {
            console.log('Successfully wrote to jobsData.json');
        }
    });

    await browser.close();
}

run();

// TODO: STUDY THIS CODE
