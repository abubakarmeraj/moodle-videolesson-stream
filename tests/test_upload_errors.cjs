// SPDX-License-Identifier: GPL-3.0-or-later
// Copyright 2026 ValeLMS contributors
const assert = require('node:assert/strict');
const {scenario} = require('./test_upload_urls.cjs');
const url = 'https://storage.example.invalid/raw/synthetic-part';
(async() => {
    const results = [];
    for (const [name, options, label, count] of [
        ['storage HTTP 500 is NOT pause', {outcomes: [500]}, 'storage', 3],
        ['storage HTTP 400', {outcomes: [400]}, 'storage', 3],
        ['authorization denied after fresh plans', {outcomes: [403]}, 'authorization', 3],
        ['network failures', {outcomes: ['network']}, 'transport', 3],
        ['timeouts', {outcomes: ['timeout']}, 'transport', 3],
        ['receipt hidden by CORS', {outcomes: ['cors']}, 'cors', 1],
        ['transient failure recovered', {outcomes: [500, 200]}, 'complete', 2],
        ['expired part authorization refreshed', {outcomes: [403, 200]}, 'complete', 2],
        ['intentional pause', {pause: true}, 'paused', 1],
        ['Moodle server failure', {rpcFailure: {action: 'part', status: 500}}, 'server', 0],
        ['Moodle auth failure', {rpcFailure: {action: 'part', status: 403}}, 'authorization', 0],
        ['Moodle transport failure', {rpcFailure: {action: 'part', network: true}}, 'transport', 0],
        ['sibling cancellation retains causal failure', {outcomes: [500], multi: true}, 'storage', null],
    ]) {
        const result = await scenario({url, ...options, pollAfter: label !== 'complete'});
        assert.equal(result.message, 'cfupload' + label, name);
        if (label !== 'complete') {
            assert.equal(result.status, 'cfstate: cfstatus' + (label === 'paused' ? 'paused' : 'failed'), name);
            assert.equal(result.progress, 0, 'poll reflects zero server-confirmed bytes on this failed/paused trial');
        }
        if (count !== null) { assert.equal(result.submitted.length, count, name); }
        assert.equal(result.controls.some(c => c.action === 'abort'), false, name);
        assert.equal(result.controls.some(c => c.action === 'complete'), label === 'complete', name);
        assert.equal(result.videoPolls, label === 'complete' ? 1 : 2, 'poll does not erase failure');
        if (label !== 'complete') { assert.ok(result.values.size, 'resume identity retained'); }
        results.push(name);
    }
    const resumed = await scenario({url, resumeParts: [{number: 1, size: 15}]});
    assert.equal(resumed.submitted.length, 0);
    assert.equal(resumed.message, 'cfuploadcomplete');
    results.push('server-confirmed completed parts are not re-uploaded');
    const uploading = await scenario({url, outcomes: [500], serverStage: 'uploading', pollAfter: true});
    assert.equal(uploading.status, 'cfstate: cfstatusfailed', 'durable upload session does not erase terminal headline');
    results.push('uploading server poll retains failed headline');
    const reload = await scenario({url, resumeParts: [{number: 1, size: 15}], serverStage: 'uploading'});
    assert.equal(reload.message, 'cfuploadcomplete', 'fresh page may resume despite prior local failure');
    assert.equal(reload.submitted.length, 0);
    results.push('fresh reload recovers server-confirmed upload without duplicate PUT');
    console.log(JSON.stringify({cases: results.length, pass: results}));
})().catch(error => { console.error(error.message); process.exitCode = 1; });
