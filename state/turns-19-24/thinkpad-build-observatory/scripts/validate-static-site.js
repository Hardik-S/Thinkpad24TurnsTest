```javascript
const fs = require('fs');
const path = require('path');

function validateStaticSite() {
  const filesToCheck = [
    'README.md',
    'index.html',
    'styles.css',
    'app.js',
    'data/runs.json',
    'data/hardware.json'
  ];

  filesToCheck.forEach(file => {
    if (!fs.existsSync(path.join(__dirname, file))) {
      console.error(`FAIL ${file} does not exist`);
    } else {
      console.log(`PASS ${file}`);
    }
  });

  const runsJsonPath = path.join(__dirname, 'data/runs.json');
  const hardwareJsonPath = path.join(__dirname, 'data/hardware.json');

  if (!fs.existsSync(runsJsonPath) || !fs.existsSync(hardwareJsonPath)) {
    console.error('FAIL data/runs.json or data/hardware.json does not exist');
  } else {
    console.log(`PASS ${runsJsonPath}`);
    console.log(`PASS ${hardwareJsonPath}`);
  }

  const checkAppJs = () => {
    try {
      require('./app.js');
      console.log('PASS node --check app.js');
    } catch (error) {
      console.error('FAIL node --check app.js', error);
    }
  };

  checkAppJs();

  const filesToScan = [
    'index.html',
    'styles.css',
    'app.js',
    'data/runs.json',
    'data/hardware.json'
  ];

  filesToScan.forEach(file => {
    const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
    if (content.includes('http://') || content.includes('https://')) {
      console.error(`FAIL ${file} contains http:// or https://`);
    } else if (content.includes('cdn.')) {
      console.error(`FAIL ${file} contains cdn.`);
    } else {
      console.log(`PASS ${file}`);
    }
  });
}

validateStaticSite();
```
