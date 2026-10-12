// ValeLMS contributors additions, GPL v3 or later. Binary upload bypasses Moodle PHP entirely.
import {get_string as getString} from 'core/str';
import {hashFile} from 'mod_videolessonstream/filehash';

/**
 * Prepare an already-saved activity, using its durable operation key.
 * @param {Object} config Module identity.
 */
export const prepare = async(config) => {
    try {
        const response = await fetch(M.cfg.wwwroot + '/mod/videolessonstream/upload.php?sesskey=' + M.cfg.sesskey, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({cmid: config.cmid, action: 'prepare'}),
        });
        if (!response.ok || !(await response.json()).ok) {
            throw new Error('Preparation unavailable');
        }
        window.location.reload();
    } catch {
        document.getElementById('vls-prepare-message').textContent = await getString('cfprovisionretryerror', 'mod_videolessonstream');
        document.getElementById('vls-prepare-retry').hidden = false;
    }
};

/**
 * Initialize a course-authorized, resumable multipart uploader.
 * @param {Object} config Course module identity; contains no permanent secrets.
 */
export const init = async(config) => {
    const input = document.getElementById('vls-upload-file');
    if (!input || input.dataset.initialized) {
        return;
    }
    input.dataset.initialized = '1';
    const button = document.getElementById('vls-upload-start');
    const progress = document.getElementById('vls-upload-progress');
    const message = document.getElementById('vls-upload-message');
    const status = document.getElementById('vls-status');
    const key = 'vls-upload-' + M.cfg.wwwroot + '-' + config.cmid;
    const labels = {};
    for (const label of ['preparing', 'paused', 'failed', 'complete', 'aborted', 'transport',
        'storage', 'authorization', 'server', 'cors', 'retrying']) {
        labels[label] = await getString('cfupload' + label, 'mod_videolessonstream');
    }
    const states = {};
    for (const state of ['draft', 'uploading', 'verifying', 'queued', 'processing', 'finalizing', 'ready',
        'failed', 'aborted', 'paused', 'unavailable']) {
        states[state] = await getString('cfstatus' + state, 'mod_videolessonstream');
    }
    const statusLabel = await getString('cfstate', 'mod_videolessonstream');
    const storageFull = await getString('cfstoragefull', 'mod_videolessonstream');
    const capacityError = await getString('cfuploadcapacity', 'mod_videolessonstream');
    const formatError = await getString('cfuploadformat', 'mod_videolessonstream');
    let stopped = false;
    // Cancellation stops sibling transfers; it does not mean the user pressed Pause.
    let outcome = null;
    let transferError = null;
    let running = false;
    let destroyed = false;
    let session;
    let timer;
    let resumable;
    let uploadable = false;
    let maximum = config.maxbytes;
    const requests = new Set();
    const call = async(action, values = {}) => {
        let response;
        try {
            response = await fetch(M.cfg.wwwroot + '/mod/videolessonstream/upload.php?sesskey=' + M.cfg.sesskey, {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({cmid: config.cmid, action, ...values}),
            });
        } catch {
            throw new Error('transport');
        }
        if (response.status === 401 || response.status === 403) {
            throw new Error('authorization');
        }
        if (response.status >= 500) {
            throw new Error('server');
        }
        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error('server');
        }
        if (!response.ok || !data.ok) {
            throw new Error(['storage_full', 'upload_capacity'].includes(data.error) ? data.error : 'server');
        }
        return data.data;
    };
    const pause = () => {
        stopped = true;
        outcome = 'paused';
        requests.forEach(xhr => xhr.abort());
        message.textContent = labels.paused;
        status.textContent = statusLabel + ': ' + states.paused;
    };
    document.getElementById('vls-upload-pause').addEventListener('click', pause);
    document.getElementById('vls-upload-abort').addEventListener('click', async() => {
        pause();
        outcome = 'aborted';
        try {
            const saved = JSON.parse(localStorage.getItem(key) || 'null');
            const upload = session?.upload || resumable?.upload || saved?.upload;
            if (upload) {
                await call('abort', {upload});
            }
            localStorage.removeItem(key);
            message.textContent = labels.aborted;
            status.textContent = statusLabel + ': ' + states.aborted;
        } catch {
            outcome = 'failed';
            message.textContent = labels.failed;
            status.textContent = statusLabel + ': ' + states.failed;
        }
    });
    const transfer = (url, blob, notify) => new Promise((resolve, reject) => {
        let target;
        try {
            target = new URL(url);
        } catch {
            reject(new Error('authorization'));
            return;
        }
        // The authenticated Moodle upload endpoint supplies the operator-configured
        // storage URL. Do not hard-code a vendor suffix: generic S3 uses that same
        // exact-part signed flow. Never accept insecure or userinfo-bearing URLs.
        if (target.protocol !== 'https:' || target.username || target.password || target.hash) {
            reject(new Error('authorization'));
            return;
        }
        const xhr = new XMLHttpRequest();
        requests.add(xhr);
        xhr.open('PUT', url);
        xhr.timeout = 900000;
        xhr.upload.onprogress = event => notify(event.loaded);
        xhr.onload = () => {
            requests.delete(xhr);
            if (xhr.status === 200 && xhr.getResponseHeader('ETag')) {
                resolve();
            } else {
                // HTTP 403 can mean expiry OR denied signing permissions; do not guess which.
                reject(new Error(xhr.status === 401 || xhr.status === 403 ? 'authorization' :
                    xhr.status === 200 ? 'cors' : 'storage'));
            }
        };
        xhr.onerror = xhr.ontimeout = () => {
            requests.delete(xhr);
            reject(new Error('transport'));
        };
        xhr.onabort = () => {
            requests.delete(xhr);
            reject(new Error('cancelled'));
        };
        xhr.send(blob);
    });
    button.addEventListener('click', async() => {
        if (running) {
            return;
        }
        const file = input.files[0];
        if (!uploadable || !file || file.size < 1 || (file.size > maximum && file.size !== resumable?.size)) {
            message.textContent = labels.failed;
            return;
        }
        running = true;
        stopped = false;
        outcome = null;
        transferError = null;
        button.disabled = true;
        try {
            message.textContent = labels.preparing;
            const duration = await new Promise((resolve, reject) => {
                const video = document.createElement('video');
                const url = URL.createObjectURL(file);
                const finish = value => {
                    clearTimeout(timeout); video.onloadedmetadata = null; video.onerror = null;
                    video.removeAttribute('src'); video.load(); URL.revokeObjectURL(url);
                    if (Number.isFinite(value) && value > 0) { resolve(value); } else { reject(new Error('format')); }
                };
                const timeout = setTimeout(() => finish(0), 30000);
                video.onloadedmetadata = () => finish(video.duration);
                video.onerror = () => finish(0);
                video.preload = 'metadata'; video.src = url;
            });
            if (resumable?.size !== file.size) {
                await call('preflight', {size: file.size, duration});
            }
            const sha256 = await hashFile(file, () => stopped || destroyed);
            const previous = JSON.parse(localStorage.getItem(key) || 'null');
            const operation = previous?.sha256 === sha256 ? previous.key :
                Array.from(crypto.getRandomValues(new Uint8Array(32)), n => n.toString(16).padStart(2, '0')).join('');
            // Persist operation identity before network I/O, never a signed URL or credential.
            localStorage.setItem(key, JSON.stringify({key: operation, sha256, size: file.size}));
            // Durable server/R2 state is authoritative, including after browser storage is cleared.
            session = resumable?.sha256 === sha256 && resumable?.size === file.size ?
                resumable : await call('start', {key: operation, sha256, size: file.size, duration});
            localStorage.setItem(key, JSON.stringify({key: operation, sha256, size: file.size, upload: session.upload}));
            if (session.state !== 'complete') {
                const completed = new Map(session.parts.map(p => [p.number, p.size]));
                const loaded = new Map();
                const pending = [];
                for (let part = 1; part <= Math.ceil(file.size / session.partsize); part++) {
                    if (!completed.has(part)) {
                        pending.push(part);
                    }
                }
                const render = () => {
                    progress.value = Math.min(70, 70 * ([...completed.values()].reduce((a, b) => a + b, 0) +
                        [...loaded.values()].reduce((a, b) => a + b, 0)) / file.size);
                    status.textContent = statusLabel + ': ' + states.uploading;
                    message.textContent = Math.floor(progress.value) + '%';
                };
                const consume = async() => {
                    while (pending.length) {
                        if (stopped) {
                            return;
                        }
                        const part = pending.shift();
                        const blob = file.slice((part - 1) * session.partsize, part * session.partsize);
                        for (let attempt = 0; attempt < 3; attempt++) {
                            try {
                                if (stopped) {
                                    throw new Error('Paused');
                                }
                                const auth = await call('part', {upload: session.upload, part});
                                if (stopped) {
                                    throw new Error('Paused');
                                }
                                await transfer(auth.url, blob, n => { loaded.set(part, n); render(); });
                                loaded.delete(part);
                                completed.set(part, blob.size);
                                render();
                                break;
                            } catch (error) {
                                loaded.delete(part);
                                if (stopped || attempt === 2 ||
                                        !['transport', 'storage', 'authorization', 'server'].includes(error.message)) {
                                    throw error;
                                }
                                message.textContent = labels.retrying;
                                await new Promise(resolve => setTimeout(resolve, 1000 * (attempt + 1)));
                            }
                        }
                    }
                };
                // Stop sibling consumers immediately, but settle them before permitting a new run.
                const consumeSafely = async() => {
                    try {
                        await consume();
                    } catch (error) {
                        // Preserve the first causal error, not a later sibling XHR abort.
                        transferError = transferError || error;
                        stopped = true;
                        requests.forEach(xhr => xhr.abort());
                        throw error;
                    }
                };
                const results = await Promise.allSettled([consumeSafely(), consumeSafely(), consumeSafely()]);
                if (results.some(result => result.status === 'rejected')) {
                    throw transferError;
                }
                if (stopped) {
                    throw new Error('Paused');
                }
                await call('complete', {upload: session.upload});
            }
            progress.value = 70;
            message.textContent = labels.complete;
        } catch (error) {
            requests.forEach(xhr => xhr.abort());
            outcome = outcome || (['transport', 'storage', 'authorization', 'server', 'cors'].includes(error.message) ?
                error.message : 'failed');
            message.textContent = outcome === 'paused' || outcome === 'aborted' ? labels[outcome] :
                error.message === 'storage_full' ? storageFull :
                error.message === 'upload_capacity' ? capacityError :
                    error.message === 'format' ? formatError : labels[outcome];
            status.textContent = statusLabel + ': ' + (outcome === 'paused' || outcome === 'aborted' ?
                states[outcome] : states.failed);
        } finally {
            running = false;
            button.disabled = !uploadable;
        }
    });
    let polls = 0;
    const poll = async() => {
        if (destroyed) {
            return;
        }
        try {
            const video = await call('video');
            resumable = video.resume || null;
            maximum = Math.min(config.maxbytes, video.maxbytes || config.maxbytes);
            uploadable = video.can_upload && ['draft', 'failed', 'uploading', 'upload-aborted'].includes(video.state);
            button.disabled = running || !uploadable;
            input.disabled = running || !uploadable;
            document.getElementById('vls-upload-pause').disabled = !running;
            document.getElementById('vls-upload-abort').disabled = !resumable && !running;
            document.getElementById('vls-processing-retry').hidden = video.state !== 'failed';
            if (!running) {
                progress.value = video.progress;
                const state = video.stage === 'upload-aborted' ? 'aborted' : video.stage;
                let label = states[state] || states.unavailable;
                // A live multipart session is resumable after a terminal browser
                // failure, not still uploading. Do not let polling contradict it.
                if (outcome && ['draft', 'uploading', 'failed', 'upload-aborted'].includes(video.state)) {
                    label = outcome === 'paused' || outcome === 'aborted' ? states[outcome] : states.failed;
                }
                if (state === 'processing' && video.qualities?.length) {
                    const heights = video.qualities.filter(h => Number.isInteger(h) && h > 0 && h <= 2160);
                    if (heights.length) {
                        label = await getString('cfstatusqualities', 'mod_videolessonstream', heights.map(h => h + 'p').join(', '));
                    }
                }
                status.textContent = statusLabel + ': ' + label;
                if (!outcome) {
                    message.textContent = Math.floor(video.progress) + '%';
                }
                if (video.state === 'ready') {
                    localStorage.removeItem(key);
                }
            }
        } catch {
            // Bounded status polling; preserve the upload's own honest result message.
        }
        timer = setTimeout(poll, polls++ < 400 ? 3000 : 15000);
    };
    void poll();
    window.addEventListener('pagehide', () => { destroyed = true; pause(); clearTimeout(timer); }, {once: true});
};
