const fs = require('fs');
const path = require('path');

const hooks = ['useState', 'useEffect', 'useRef', 'useCallback', 'useMemo'];

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(function(file) {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) { 
            results = results.concat(walk(file));
        } else {
            if (file.endsWith('.tsx') || file.endsWith('.ts')) {
                results.push(file);
            }
        }
    });
    return results;
}

const files = walk('c:/Users/User/Desktop/clubs/clubs/msu_platform/frontend/src');

for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    
    // Check if any hook is used
    let usedHooks = [];
    for (const hook of hooks) {
        // Find usages like `useState(` or `useState<`
        if (new RegExp(`\\b${hook}\\b\\s*[<(]`).test(content)) {
            usedHooks.push(hook);
        }
    }
    
    if (usedHooks.length > 0) {
        // Check if react imports them
        // import { useState } from 'react';
        // import React, { useState } from 'react';
        let missing = [];
        for (const hook of usedHooks) {
            // Very naive check: does the file contain "hook" and "react"?
            // A better check:
            const importRegex = new RegExp(`import\\s+.*\\b${hook}\\b.*from\\s+['"]react['"]`);
            if (!importRegex.test(content)) {
                // Check if they use React.useState instead
                const reactDotRegex = new RegExp(`React\\.${hook}`);
                if (!reactDotRegex.test(content)) {
                   missing.push(hook);
                }
            }
        }
        
        if (missing.length > 0) {
            console.log(`Missing imports in ${file}: ${missing.join(', ')}`);
        }
    }
}
