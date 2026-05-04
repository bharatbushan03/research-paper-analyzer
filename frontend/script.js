// ===== DOM Elements =====
const uploadView = document.getElementById('uploadView');
const analysisView = document.getElementById('analysisView');

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const uploadTitle = document.getElementById('uploadTitle');
const uploadSubtitle = document.getElementById('uploadSubtitle');
const processBtn = document.getElementById('processBtn');

const paperTitle = document.getElementById('paperTitle');
const paperMeta = document.getElementById('paperMeta');
const analysisLoading = document.getElementById('analysisLoading');
const loaderSub = document.getElementById('loaderSub');
const analysisSections = document.getElementById('analysisSections');
const chatSection = document.getElementById('chatSection');

const chatInput = document.getElementById('chatInput');
const chatSendBtn = document.getElementById('chatSendBtn');
const chatLog = document.getElementById('chatLog');
const backToUpload = document.getElementById('backToUpload');

// ===== State =====
let selectedFile = null;

// Configure marked.js options
marked.setOptions({
    breaks: true,
    gfm: true
});

// ===== View Navigation =====
function showView(view) {
    [uploadView, analysisView].forEach(v => v.classList.remove('active'));
    view.classList.add('active');
    window.scrollTo(0, 0);
}

// ===== UPLOAD LOGIC =====
fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

function handleFileSelect(file) {
    if (!file || file.type !== "application/pdf") {
        alert("Please upload a valid PDF file.");
        return;
    }
    selectedFile = file;
    uploadTitle.textContent = file.name;
    uploadSubtitle.textContent = (file.size / 1024 / 1024).toFixed(2) + " MB";
    processBtn.classList.remove('hidden');
}

processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    // Swap to Analysis View
    showView(analysisView);

    paperTitle.textContent = selectedFile.name;
    paperMeta.textContent = "Processing local document...";

    // Show loading
    analysisLoading.classList.remove('hidden');
    analysisSections.classList.add('hidden');
    chatSection.classList.add('hidden');

    const steps = [
        'Saving file to server...',
        'Extracting text from PDF...',
        'Building AI knowledge base...',
        'Generating insights (Summary, Findings, Method)...'
    ];

    let stepIdx = 0;
    const stepInterval = setInterval(() => {
        stepIdx = Math.min(stepIdx + 1, steps.length - 1);
        loaderSub.textContent = steps[stepIdx];
    }, 4000);

    try {
        const res = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        clearInterval(stepInterval);
        const data = await res.json();

        if (res.ok && data.analysis) {
            renderSection('summaryText', data.analysis.summary);
            renderSection('findingsText', data.analysis.key_findings);
            renderSection('methodText', data.analysis.methodology);
            renderSection('conclusionText', data.analysis.conclusion);

            paperMeta.textContent = "Analysis Complete";

            analysisLoading.classList.add('hidden');
            analysisSections.classList.remove('hidden');
            chatSection.classList.remove('hidden');
            chatLog.innerHTML = '';
        } else {
            const errMsg = data.error || 'Could not analyze this paper.';
            analysisLoading.classList.add('hidden');
            analysisSections.classList.remove('hidden');
            renderSection('summaryText', `**Error:** ${errMsg}`);
            paperMeta.textContent = "Analysis Failed";
        }

    } catch (err) {
        clearInterval(stepInterval);
        console.error('Upload error:', err);
        analysisLoading.classList.add('hidden');
        analysisSections.classList.remove('hidden');
        renderSection('summaryText', '**Error:** Could not connect to server.');
        paperMeta.textContent = "Connection Error";
    }
});

function renderSection(id, content) {
    const el = document.getElementById(id);
    if (content) {
        el.innerHTML = marked.parse(content);
    } else {
        el.textContent = 'Not available';
    }
}

// ===== FOLLOW-UP CHAT =====
async function askFollowUp() {
    const question = chatInput.value.trim();
    if (!question) return;

    addChatMsg('user', question);
    chatInput.value = '';

    const thinkingEl = addChatMsg('assistant', 'Thinking...');

    try {
        const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await res.json();

        if (res.ok) {
            thinkingEl.innerHTML = marked.parse(data.answer);
        } else {
            thinkingEl.textContent = data.error || 'Could not get an answer.';
        }
    } catch (err) {
        thinkingEl.textContent = 'Connection error.';
    }
}

function addChatMsg(role, text) {
    const msg = document.createElement('div');
    msg.className = `chat-msg ${role}`;
    if (role === 'assistant' && text !== 'Thinking...') {
        msg.innerHTML = marked.parse(text);
    } else {
        msg.textContent = text;
    }
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
    return msg;
}

// ===== UTILITIES =====
function copyText(elementId) {
    const element = document.getElementById(elementId);
    const text = element.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        const btn = element.parentElement.querySelector('.copy-btn');
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.color = 'var(--emerald)';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}

// ===== Additional Event Listeners =====
chatSendBtn.addEventListener('click', askFollowUp);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') askFollowUp();
});

backToUpload.addEventListener('click', () => {
    selectedFile = null;
    uploadTitle.textContent = "Select a PDF File";
    uploadSubtitle.textContent = "Click to browse or drag & drop here";
    processBtn.classList.add('hidden');
    showView(uploadView);
});