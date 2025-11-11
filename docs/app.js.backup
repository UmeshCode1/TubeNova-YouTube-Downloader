// TubeNova Frontend
// Core UI logic: info fetch, streaming download with progress, history, theme, animations

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const state = {
  meta: null,
  formats: [],
  downloadsThisSession: Number(sessionStorage.getItem('tn_downloads') || '0'),
};

const BACKEND = () => (window.BACKEND_URL || 'http://127.0.0.1:5000').replace(/\/$/, '');

function toast(msg, type = 'info') {
  const el = $('#toast');
  el.innerHTML = `<div class="card p-3 rounded-xl bg-black/70 border border-white/10 text-sm ${type==='error'?'text-red-300':'text-white'}">${msg}</div>`;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 2500);
}

function fmtDuration(sec) {
  if (!sec && sec !== 0) return '';
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = Math.floor(sec % 60);
  return [h, m, s].filter((v,i) => v || i>0).map(v => String(v).padStart(2,'0')).join(':');
}

function saveHistory(item) {
  const key = 'tn_history';
  const arr = JSON.parse(localStorage.getItem(key) || '[]');
  arr.unshift(item);
  localStorage.setItem(key, JSON.stringify(arr.slice(0, 12)));
  renderHistory();
}

function renderHistory() {
  const key = 'tn_history';
  const arr = JSON.parse(localStorage.getItem(key) || '[]');
  const ul = $('#historyList');
  ul.innerHTML = '';
  arr.forEach(x => {
    const li = document.createElement('li');
    li.className = 'flex items-center gap-2';
    li.innerHTML = `<img src="${x.thumbnail}" class="w-10 h-10 rounded object-cover" alt="thumb"/>` +
      `<div class="min-w-0 flex-1"><p class="truncate">${x.title}</p><p class="text-xs text-slate-400">${x.quality} · ${x.type}</p></div>` +
      `<a class="text-neon-blue text-xs" href="${x.url}" target="_blank">Open</a>`;
    ul.appendChild(li);
  });
}

function setAnalytics() {
  $('#analytics').textContent = `Downloads this session: ${state.downloadsThisSession}`;
}

function autoPickQuality(type) {
  // Simple heuristic using NetworkInformation API
  const ni = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (type === 'audio') return '128k';
  if (ni && ni.effectiveType) {
    switch (ni.effectiveType) {
      case 'slow-2g':
      case '2g': return '144p';
      case '3g': return '360p';
      case '4g': default: return '720p';
    }
  }
  return '720p';
}

function setDarkMode(on) {
  const root = document.documentElement;
  if (on) root.classList.add('dark'); else root.classList.remove('dark');
  localStorage.setItem('tn_theme', on ? 'dark' : 'light');
  $('#themeLabel').textContent = on ? 'Light' : 'Dark';
}

function initTheme() {
  const saved = localStorage.getItem('tn_theme');
  setDarkMode(saved ? saved === 'dark' : true);
}

function initAnimations() {
  if (!window.gsap) return;
  gsap.from('header', { opacity: 0, y: -20, duration: 0.6, ease: 'power2.out' });
  gsap.from('main section', { opacity: 0, y: 20, duration: 0.6, delay: 0.1, ease: 'power2.out' });
}

function playClickSound() {
  // gentle synth using WebAudio
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(660, ctx.currentTime);
    g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.02, ctx.currentTime + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.12);
    o.connect(g).connect(ctx.destination);
    o.start(); o.stop(ctx.currentTime + 0.15);
  } catch {}
}

async function fetchInfo() {
  const url = $('#ytUrl').value.trim();
  if (!url) return toast('Please paste a YouTube link', 'error');
  $('#progressLabel').textContent = 'Fetching info…';
  $('#progressBar').style.width = '15%';
  try {
    const r = await fetch(`${BACKEND()}/api/info?url=${encodeURIComponent(url)}`);
    if (!r.ok) throw new Error('Failed to fetch info');
    const data = await r.json();
  state.meta = data;
  state.formats = data.formats || [];

    // Update UI
    $('#skeleton').classList.add('hidden');
    $('#metaCard').classList.remove('hidden');
    $('#thumb').src = data.thumbnail;
    $('#title').textContent = data.title;
    $('#channel').textContent = data.uploader || '';
    $('#duration').textContent = `Duration: ${fmtDuration(data.duration)}`;

  // Preview: use YouTube Privacy-Enhanced Mode embed
    // For simplicity, show thumbnail; when user clicks preview, try to set src to youtube embed
    const preview = $('#preview');
    preview.src = `https://www.youtube-nocookie.com/embed/${data.id}`;

  // Build dynamic quality options
  buildQualityOptions();

  // Recommend dummy
    renderRecommendations(data.title);

    // Enable download
    $('#downloadBtn').disabled = false;

    // Reset progress UI
    $('#progressLabel').textContent = 'Ready';
    $('#progressBar').style.width = '0%';

    toast('Info loaded');
  } catch (e) {
    console.error(e);
    toast('Error: could not fetch info', 'error');
    $('#progressLabel').textContent = 'Error';
    $('#progressBar').style.width = '0%';
  }
}

function findFormatId(type, quality) {
  if (!state.formats || !state.formats.length) return null;
  if (quality === 'auto') quality = autoPickQuality(type);
  // Prefer exact match by label and type
  const exact = state.formats.find(f => f.type === type && f.label === quality);
  if (exact) return exact.format_id;
  // Fallback: choose nearest lower for video, lower for audio
  if (type === 'video') {
    const order = ['144p','240p','360p','480p','720p','1080p'];
    const idx = order.indexOf(quality);
    for (let i = idx; i >= 0; i--) {
      const f = state.formats.find(x => x.type==='video' && x.label===order[i]);
      if (f) return f.format_id;
    }
  } else {
    const order = ['128k','320k'];
    const idx = order.indexOf(quality);
    for (let i = idx; i >= 0; i--) {
      const f = state.formats.find(x => x.type==='audio' && x.label===order[i]);
      if (f) return f.format_id;
    }
  }
  // Final fallback: first available of type
  const any = state.formats.find(f => f.type === type);
  return any ? any.format_id : null;
}

async function downloadSelected() {
  const url = $('#ytUrl').value.trim();
  const type = $('#typeSelect').value;
  const quality = $('#qualitySelect').value;
  if (!state.meta) return toast('Fetch info first', 'error');
  const format_id = findFormatId(type, quality);
  if (!format_id) return toast('Selected quality not available', 'error');

  playClickSound();

  $('#progressLabel').textContent = 'Downloading…';
  $('#progressBar').style.width = '5%';

  const dlUrl = `${BACKEND()}/api/download?url=${encodeURIComponent(url)}&format_id=${encodeURIComponent(format_id)}`;

  try {
    const res = await fetch(dlUrl);
    if (!res.ok || !res.body) throw new Error('Download failed');

    const reader = res.body.getReader();
    const contentLength = Number(res.headers.get('Content-Length') || '0');
    const chunks = [];
    let received = 0;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      received += value.length;
      if (contentLength) {
        const pct = Math.min(100, Math.round(received * 100 / contentLength));
        $('#progressBar').style.width = pct + '%';
        $('#progressLabel').textContent = `Downloading… ${pct}%`;
      } else {
        const base = Math.min(95, 5 + Math.round(received / (1024*256)));
        $('#progressBar').style.width = base + '%';
      }
    }

    const blob = new Blob(chunks, { type: 'application/octet-stream' });
    const a = document.createElement('a');
    const urlObj = URL.createObjectURL(blob);
    a.href = urlObj;
    const safeTitle = (state.meta.title || 'tubenova').replace(/[^\w\-\s\(\)\[\]]+/g, '_').slice(0, 80);
    const ext = type === 'audio' ? 'm4a' : 'mp4';
    a.download = `${safeTitle}_${quality}.${ext}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(urlObj);

    // Confetti
    if (window.confetti) {
      confetti({ particleCount: 160, spread: 70, origin: { y: 0.2 } });
    }

    state.downloadsThisSession += 1;
    sessionStorage.setItem('tn_downloads', String(state.downloadsThisSession));
    setAnalytics();

    saveHistory({
      title: state.meta.title,
      thumbnail: state.meta.thumbnail,
      url: state.meta.webpage_url,
      type, quality
    });

    toast('Download complete ✅');
    $('#progressLabel').textContent = 'Done';
    $('#progressBar').style.width = '100%';
    setTimeout(() => { $('#progressBar').style.width = '0%'; }, 800);
  } catch (e) {
    console.error(e);
    toast('Download failed', 'error');
    $('#progressLabel').textContent = 'Error';
    $('#progressBar').style.width = '0%';
  }
}

function renderRecommendations(title='') {
  const reco = $('#reco');
  reco.innerHTML = '';
  // Dummy AI: create 4 cards with themed placeholders
  const keywords = (title || 'Tech Music Travel Gaming').split(/\s+/).slice(0,4);
  for (let i=0;i<4;i++) {
    const k = keywords[i] || 'Trends';
    const t = `${k} Highlights ${2020 + (i%6)}`;
    const thumb = `https://picsum.photos/seed/${encodeURIComponent(k+i)}/300/180`;
    const card = document.createElement('a');
    card.href = '#';
    card.className = 'block rounded-xl overflow-hidden border border-white/10 bg-black/30 hover:bg-black/40 transition';
    card.innerHTML = `<img src="${thumb}" class="w-full aspect-video object-cover" alt="${t}">`+
      `<div class="p-2 text-sm truncate">${t}</div>`;
    reco.appendChild(card);
  }
}

function wireEvents() {
  $('#fetchBtn').addEventListener('click', fetchInfo);
  $('#downloadBtn').addEventListener('click', downloadSelected);
  $('#copyBtn').addEventListener('click', () => {
    const v = $('#ytUrl').value.trim();
    if (!v) return toast('Nothing to copy', 'error');
    navigator.clipboard.writeText(v);
    toast('Link copied');
  });
  $('#waBtn').addEventListener('click', (e) => {
    const v = $('#ytUrl').value.trim();
    if (!v) return toast('Paste a link first', 'error');
    const u = `https://wa.me/?text=${encodeURIComponent('Check this video: '+v)}`;
    $('#waBtn').href = u;
  });
  $('#themeToggle').addEventListener('click', () => setDarkMode(!document.documentElement.classList.contains('dark')));
  $('#backendBtn').addEventListener('click', () => {
    const current = window.BACKEND_URL || 'http://127.0.0.1:5000';
    const v = prompt('Set backend base URL (e.g. https://tubenova.onrender.com)', current);
    if (v && /^https?:\/\//i.test(v)) {
      localStorage.setItem('tubenova_backend_url', v);
      window.BACKEND_URL = v;
      toast('Backend URL saved');
    } else if (v) {
      toast('Invalid URL', 'error');
    }
  });

  // Change quality group visibility based on type (optional enhancement)
  $('#typeSelect').addEventListener('change', () => {
    buildQualityOptions();
  });
}

function boot() {
  initTheme();
  initAnimations();
  renderHistory();
  setAnalytics();
}

document.addEventListener('DOMContentLoaded', () => {
  wireEvents();
  boot();
});

function buildQualityOptions() {
  const sel = $('#qualitySelect');
  const t = $('#typeSelect').value;
  const current = sel.value;
  const opts = [];
  opts.push({value: 'auto', label: 'Auto (recommended)'});
  if (!state.formats || !state.formats.length) {
    // fallback to static
    if (t === 'video') {
      ['144p','240p','360p','480p','720p','1080p'].forEach(v=>opts.push({value:v,label:v}));
    } else {
      ['128k','320k'].forEach(v=>opts.push({value:v,label:v.replace('k',' kbps')}));
    }
  } else {
    const list = state.formats.filter(f=>f.type===t);
    const labels = Array.from(new Set(list.map(f=>f.label)));
    const ordered = t==='video' ? ['144p','240p','360p','480p','720p','1080p'] : ['128k','320k'];
    ordered.forEach(v => { if (labels.includes(v)) opts.push({value:v,label: t==='video'? v : (v.replace('k',' kbps'))}); });
  }
  sel.innerHTML = '';
  for (const o of opts) {
    const opt = document.createElement('option');
    opt.value = o.value; opt.textContent = o.label; sel.appendChild(opt);
  }
  // try to keep previous choice
  if ([...sel.options].some(o=>o.value===current)) sel.value = current;
}
