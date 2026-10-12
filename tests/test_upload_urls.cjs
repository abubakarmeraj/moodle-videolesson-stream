// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors
// Exercise the real compiled uploader through its authenticated part-plan flow.
// Synthetic URLs and in-memory DOM/XHR doubles only; no network or secrets.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {webcrypto} = require('node:crypto');
const source = fs.readFileSync(process.env.VALELMS_UPLOAD_AMD ||
    path.join(__dirname, '../plugin/mod_videolessonstream/amd/build/upload.min.js'), 'utf8');

async function scenario({url, authorized = true, injected = false, outcomes = [], rpcFailure, pause = false,
    resumeParts = [], multi = false, pollAfter = false, serverStage = 'draft'}) {
    const nodes = new Map();
    const file = new Blob(['synthetic video'], {type: 'video/mp4'});
    const submitted = [];
    const controls = [];
    const timers = [];
    let transfers = 0;
    let videoPolls = 0;
    const node = id => {
        if (!nodes.has(id)) {
            nodes.set(id, {dataset: {}, value: 0, files: [file], handlers: {},
                addEventListener(event, fn) { this.handlers[event] = fn; }});
        }
        return nodes.get(id);
    };
    const values = new Map();
    if (injected) {
        values.set('vls-upload-https://moodle.example.invalid-42', JSON.stringify({
            url: 'https://unexpected.example.invalid/stolen', upload: 'untrusted-input',
            key: 'bad', sha256: 'different', size: file.size,
        }));
    }
    let module;
    const context = vm.createContext({
        URL, Blob, Uint8Array, crypto: webcrypto, console,
        M: {cfg: {wwwroot: 'https://moodle.example.invalid', sesskey: 'synthetic-session'}},
        setTimeout(fn, delay) {
            if (delay <= 2000) { queueMicrotask(fn); }
            if (delay === 3000) { timers.push(fn); }
            return 1;
        },
        clearTimeout() {},
        window: {addEventListener() {}, location: {reload() {}}},
        localStorage: {getItem: key => values.get(key), setItem: (key, value) => values.set(key, value),
            removeItem: key => values.delete(key)},
        document: {getElementById: node, createElement() {
            return {duration: 30, removeAttribute() {}, load() {},
                set src(value) { queueMicrotask(() => this.onloadedmetadata?.()); }};
        }},
        fetch: async(endpoint, options) => {
            assert.equal(endpoint, 'https://moodle.example.invalid/mod/videolessonstream/upload.php?sesskey=synthetic-session');
            assert.equal(options.method, 'POST');
            const request = JSON.parse(options.body);
            controls.push(request);
            if (request.action === rpcFailure?.action) {
                if (rpcFailure.network) { throw new Error('synthetic transport error'); }
                return {ok: false, status: rpcFailure.status, json: async() => ({ok: false, error: 'sensitive-untrusted-error'})};
            }
            let data;
            if (request.action === 'video') {
                data = {state: serverStage, can_upload: true, maxbytes: 512 * 1024**2, stage: serverStage, progress: 0};
                videoPolls++;
            } else if (request.action === 'start') {
                data = {upload: 'service-session', state: 'uploading', parts: resumeParts,
                    partsize: multi ? 5 : 8 * 1024**2};
            } else if (request.action === 'part') {
                assert.equal(request.upload, 'service-session');
                assert.ok(request.part >= 1 && request.part <= 3);
                assert.equal('url' in request, false);
                data = {url};
                return {ok: authorized, status: authorized ? 200 : 403, json: async() => ({ok: authorized, data})};
            } else {
                data = {};
            }
            return {ok: true, json: async() => ({ok: true, data})};
        },
        XMLHttpRequest: class {
            constructor() { this.upload = {}; }
            open(method, destination) { assert.equal(method, 'PUT'); this.destination = destination; }
            send(body) {
                submitted.push(this.destination);
                const result = outcomes[Math.min(transfers++, outcomes.length - 1)] || 200;
                this.status = typeof result === 'number' ? result : 200;
                this.receipt = result !== 'cors';
                queueMicrotask(() => {
                    if (this.aborted) { return; }
                    this.upload.onprogress?.({loaded: body.size});
                    if (pause) { node('vls-upload-pause').handlers.click(); return; }
                    if (result === 'network') { this.onerror(); }
                    else if (result === 'timeout') { this.ontimeout(); }
                    else { this.onload(); }
                });
            }
            getResponseHeader(name) { assert.equal(name, 'ETag'); return this.receipt ? 'synthetic-etag' : null; }
            abort() { this.aborted = true; this.onabort?.(); }
        },
        define(name, dependencies, factory) {
            assert.equal(name, 'mod_videolessonstream/upload');
            module = {};
            factory(module, {get_string: async(key) => key}, {hashFile: async() => 'a'.repeat(64)});
        },
    });
    vm.runInContext(source, context);
    await module.init({cmid: 42, maxbytes: 512 * 1024**2, url: 'https://unexpected.example.invalid/config'});
    await new Promise(resolve => setImmediate(resolve));
    await node('vls-upload-start').handlers.click();
    if (pollAfter) { await timers.shift()?.(); }
    return {submitted, controls, message: node('vls-upload-message').textContent,
        status: node('vls-status').textContent, progress: node('vls-upload-progress').value, values, videoPolls};
}

async function main() {
    const cases = [
        ['generic S3 HTTPS', 'https://storage.example.invalid/raw/key?partNumber=1&X-Amz-Signature=synthetic', true],
        ['historical R2 HTTPS', 'https://' + '0'.repeat(32) + '.r2.cloudflarestorage.com/raw/key?partNumber=1', true],
        ['production HTTP', 'http://storage.example.invalid/raw/key', false],
        ['URL username/password', 'https://user:password@storage.example.invalid/raw/key', false],
        ['URL fragment', 'https://storage.example.invalid/raw/key#fragment', false],
        ['malformed URL', 'not a URL', false],
        ['relative URL', '/raw/key', false],
        ['non-HTTPS scheme', 'file:///tmp/key', false],
    ];
    const results = [];
    for (const [name, url, allowed] of cases) {
        const result = await scenario({url});
        assert.equal(result.submitted.length, allowed ? 1 : 0, name);
        if (allowed) { assert.equal(result.submitted[0], url); }
        results.push({name, pass: true});
    }
    const failedPlan = await scenario({url: 'https://unexpected.example.invalid/key', authorized: false});
    assert.equal(failedPlan.submitted.length, 0);
    results.push({name: 'unauthenticated/failed upload plan cannot authorize PUT', pass: true});
    const injected = await scenario({url: 'https://storage.example.invalid/key', injected: true});
    assert.deepEqual(injected.submitted, ['https://storage.example.invalid/key']);
    results.push({name: 'config/file/localStorage destination cannot replace server plan', pass: true});
    console.log(JSON.stringify({cases: results.length, results}));
}
module.exports = {scenario};
if (require.main === module) {
    main().catch(error => { console.error(error.message); process.exitCode = 1; });
}
