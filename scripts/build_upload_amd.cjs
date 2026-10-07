// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors
// Rebuild the component's AMD modules/maps; dependencies are pinned in scripts/amd.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {createRequire} = require('node:module');
const requireBuild = createRequire(path.join(__dirname, 'amd/package.json'));
const babel = requireBuild('@babel/core');
const terser = requireBuild('terser');
const root = path.resolve(__dirname, '..');
const destination = path.resolve(process.argv[2] || path.join(root, 'plugin/mod_videolessonstream/amd/build'));

(async() => {
    fs.mkdirSync(destination, {recursive: true});
    const hashes = {};
    const sourceDir = path.join(root, 'plugin/mod_videolessonstream/amd/src');
    for (const filename of fs.readdirSync(sourceDir).filter(name => name.endsWith('.js')).sort()) {
    const name = filename.slice(0, -3);
    const source = fs.readFileSync(path.join(sourceDir, filename), 'utf8');
    const transformed = babel.transformSync(source, {
        filename, moduleId: `mod_videolessonstream/${name}`,
        babelrc: false, configFile: false,
        plugins: [requireBuild.resolve('@babel/plugin-transform-modules-amd')],
        sourceMaps: true, sourceFileName: `../src/${filename}`,
    });
    const result = await terser.minify(transformed.code, {
        sourceMap: {content: transformed.map, filename: `${name}.min.js`, url: `${name}.min.js.map`},
        format: {comments: false},
    });
    for (const [outputName, contents] of [[`${name}.min.js`, result.code], [`${name}.min.js.map`, result.map]]) {
        const bytes = Buffer.from(contents + '\n');
        fs.writeFileSync(path.join(destination, outputName), bytes);
        hashes[outputName] = crypto.createHash('sha256').update(bytes).digest('hex');
    }
    }
    console.log(JSON.stringify({node: process.version, babel: babel.version,
        transformModulesAmd: requireBuild('@babel/plugin-transform-modules-amd/package.json').version,
        terser: requireBuild('terser/package.json').version, hashes}));
})().catch(() => { console.error('Uploader AMD build failed'); process.exitCode = 1; });
