// This module is completely unused and should be detected as dead

function orphanedFunction() {
    // This function is in an orphaned file
    return "This file is never imported";
}

class OrphanedClass {
    constructor() {
        this.value = 42;
    }
    
    method() {
        return this.value * 2;
    }
}

module.exports = {
    orphanedFunction,
    OrphanedClass
};