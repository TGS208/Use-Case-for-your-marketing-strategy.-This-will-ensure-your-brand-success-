// Data processing module

class DataProcessor {
    constructor() {
        this.processedCount = 0;
    }
    
    processData(filename) {
        console.log(`Processing data from ${filename}`);
        this.processedCount++;
        return true;
    }
    
    unusedMethod() {
        // This method is never called - dead code
        return "Unused method";
    }
}

module.exports = DataProcessor;