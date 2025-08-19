// Utility functions for JavaScript application

function helperFunction(data) {
    console.log(`Processing: ${data}`);
    return data.toUpperCase();
}

function unusedFunction() {
    // This function is defined but never used - dead code
    return "This is never called";
}

// This constant is also unused
const UNUSED_CONSTANT = "This constant is never used";

module.exports = {
    helperFunction
    // Note: unusedFunction and UNUSED_CONSTANT are not exported or used
};