// Main JavaScript application entry point
const { helperFunction } = require('./utils');
const DataProcessor = require('./data-processor');

function main() {
    console.log('Starting JavaScript application...');
    helperFunction('test data');
    
    const processor = new DataProcessor();
    processor.processData('sample.txt');
    
    console.log('Application completed.');
}

if (require.main === module) {
    main();
}

module.exports = { main };