// TubeNova Enhanced Features
// Additional cartoon-style UI enhancements and new features

// Enhanced state management
const enhancedState = {
  totalDownloadSize: 0,
  reactions: {},
  playlistMode: false,
  currentTab: 'single'
};

// Fun emoji reactions
const reactionEmojis = {
  like: '👍',
  love: '❤️',
  fire: '🔥',
  party: '🎉'
};

// Progress emoji mapper
const progressEmojis = {
  idle: '💤',
  fetching: '🔍',
  downloading: '⬇️',
  processing: '⚙️',
  complete: '✅',
  error: '❌'
};

// Update progress emoji
function updateProgressEmoji(status) {
  const emoji = progressEmojis[status] || '💤';
  const el = $('#progressEmoji');
  if (el) el.textContent = emoji;
}

// Paste from clipboard
async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    $('#ytUrl').value = text;
    toast('📋 Link pasted!', 'info');
    playSound('click');
  } catch (e) {
    toast('⚠️ Clipboard access denied', 'error');
  }
}

// Load example video
function loadExample(url) {
  $('#ytUrl').value = url;
  toast('✨ Example loaded! Click Fetch.', 'info');
  playSound('pop');
}

// Toggle advanced options
function toggleAdvanced() {
  const opts = $('#advancedOptions');
  const arrow = $('#advancedArrow');
  if (opts.classList.contains('hidden')) {
    opts.classList.remove('hidden');
    arrow.textContent = '▲';
  } else {
    opts.classList.add('hidden');
    arrow.textContent = '▼';
  }
}

// Show/hide trim controls
function toggleTrimControls() {
  const trimControls = $('#trimControls');
  const trimCheckbox = $('#trimVideo');
  if (trimCheckbox.checked) {
    trimControls.classList.remove('hidden');
  } else {
    trimControls.classList.add('hidden');
  }
}

// Download thumbnail
async function downloadThumbnail() {
  if (!state.meta || !state.meta.thumbnail) {
    return toast('❌ Fetch video info first!', 'error');
  }
  
  try {
    playSound('download');
    const response = await fetch(state.meta.thumbnail);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${sanitizeFilename(state.meta.title)}_thumbnail.jpg`;
    a.click();
    URL.revokeObjectURL(url);
    
    toast('🖼️ Thumbnail downloaded!', 'info');
    showReaction('party');
  } catch (e) {
    toast('❌ Thumbnail download failed', 'error');
  }
}

// Show video info modal (simplified)
function showVideoInfo() {
  if (!state.meta) {
    return toast('❌ Fetch video info first!', 'error');
  }
  
  const info = `
📺 Title: ${state.meta.title}
👤 Channel: ${state.meta.uploader}
⏱️ Duration: ${fmtDuration(state.meta.duration)}
🆔 Video ID: ${state.meta.id}
  `.trim();
  
  alert(info);
  playSound('info');
}

// Play preview
function playPreview() {
  const container = $('#previewContainer');
  const preview = $('#preview');
  
  if (container.classList.contains('hidden')) {
    container.classList.remove('hidden');
    preview.src = `https://www.youtube-nocookie.com/embed/${state.meta.id}?autoplay=1`;
    playSound('play');
  } else {
    container.classList.add('hidden');
    preview.src = '';
  }
}

// Reaction animation
function showReaction(type) {
  const overlay = $('#reactionOverlay');
  const emoji = reactionEmojis[type] || '✨';
  
  for (let i = 0; i < 15; i++) {
    setTimeout(() => {
      const el = document.createElement('div');
      el.textContent = emoji;
      el.className = 'fixed text-4xl pointer-events-none';
      el.style.left = Math.random() * window.innerWidth + 'px';
      el.style.top = window.innerHeight + 'px';
      el.style.animation = `reactionFloat ${2 + Math.random()}s ease-out forwards`;
      overlay.appendChild(el);
      
      setTimeout(() => el.remove(), 3000);
    }, i * 100);
  }
}

// Add CSS animation for reactions
const style = document.createElement('style');
style.textContent = `
@keyframes reactionFloat {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(-${window.innerHeight}px) rotate(360deg); opacity: 0; }
}
`;
document.head.appendChild(style);

// Simple sound effects using Web Audio API
function playSound(type) {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    
    const sounds = {
      click: { freq: 800, duration: 0.05 },
      pop: { freq: 1000, duration: 0.1 },
      download: { freq: 600, duration: 0.15 },
      success: { freq: 1200, duration: 0.2 },
      error: { freq: 200, duration: 0.3 },
      info: { freq: 900, duration: 0.08 },
      play: { freq: 700, duration: 0.12 }
    };
    
    const sound = sounds[type] || sounds.click;
    o.type = 'sine';
    o.frequency.setValueAtTime(sound.freq, ctx.currentTime);
    g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.015, ctx.currentTime + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + sound.duration);
    o.connect(g).connect(ctx.destination);
    o.start();
    o.stop(ctx.currentTime + sound.duration + 0.1);
  } catch {}
}

// Clear history
function clearHistory() {
  if (confirm('🗑️ Clear all download history?')) {
    localStorage.removeItem('tn_history');
    renderHistory();
    toast('✅ History cleared!', 'info');
    playSound('click');
  }
}

// Enhanced theme toggle with emoji
function toggleTheme() {
  const isDark = document.documentElement.classList.contains('dark');
  setDarkMode(!isDark);
  const icon = $('#themeIcon');
  icon.textContent = isDark ? '☀️' : '🌙';
  playSound('pop');
}

// Tab switching
function switchTab(tabName) {
  enhancedState.currentTab = tabName;
  
  // Update tab buttons
  $$('.tab-btn').forEach(btn => {
    btn.classList.remove('bg-neon-pink/30', 'border-neon-pink', 'text-white', 'font-semibold');
    btn.classList.add('bg-white/10', 'border-white/20', 'text-slate-300');
  });
  
  const activeBtn = $(`#tab${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`);
  if (activeBtn) {
    activeBtn.classList.add('bg-neon-pink/30', 'border-neon-pink', 'text-white', 'font-semibold');
    activeBtn.classList.remove('bg-white/10', 'border-white/20', 'text-slate-300');
  }
  
  toast(`Switched to ${tabName} mode 🎯`, 'info');
  playSound('click');
}

// Enhanced stats
function updateStats() {
  const downloads = state.downloadsThisSession;
  const size = (enhancedState.totalDownloadSize / (1024 * 1024)).toFixed(1);
  
  $('#statsDownloads').textContent = downloads;
  $('#statsSize').textContent = `${size} MB`;
}

// Sanitize filename
function sanitizeFilename(name) {
  return name.replace(/[^\w\s\-\(\)\[\]]/g, '_').slice(0, 80);
}

// Enhanced progress display
function updateProgress(percent, speed, eta) {
  const bar = $('#progressBar');
  const label = $('#progressPercent');
  const speedEl = $('#downloadSpeed');
  const etaEl = $('#downloadETA');
  
  if (bar) bar.style.width = percent + '%';
  if (label) label.textContent = Math.round(percent) + '%';
  if (speedEl && speed) speedEl.textContent = `${(speed / 1024).toFixed(1)} KB/s`;
  if (etaEl && eta) etaEl.textContent = `ETA: ${Math.round(eta)}s`;
}

// Wire up new event listeners
function wireEnhancedEvents() {
  // Paste button
  const pasteBtn = $('#pasteBtn');
  if (pasteBtn) pasteBtn.addEventListener('click', pasteFromClipboard);
  
  // Example buttons
  const ex1 = $('#exampleBtn1');
  const ex2 = $('#exampleBtn2');
  if (ex1) ex1.addEventListener('click', () => loadExample('https://www.youtube.com/watch?v=dQw4w9WgXcQ'));
  if (ex2) ex2.addEventListener('click', () => loadExample('https://www.youtube.com/shorts/abc123'));
  
  // Advanced options toggle
  const advToggle = $('#advancedToggle');
  if (advToggle) advToggle.addEventListener('click', toggleAdvanced);
  
  // Trim checkbox
  const trimCheckbox = $('#trimVideo');
  if (trimCheckbox) trimCheckbox.addEventListener('change', toggleTrimControls);
  
  // Thumbnail download
  const thumbBtn = $('#thumbnailBtn');
  if (thumbBtn) thumbBtn.addEventListener('click', downloadThumbnail);
  
  // Info button
  const infoBtn = $('#infoBtn');
  if (infoBtn) infoBtn.addEventListener('click', showVideoInfo);
  
  // Play preview
  const playBtn = $('#playPreview');
  if (playBtn) playBtn.addEventListener('click', playPreview);
  
  // Clear history
  const clearBtn = $('#clearHistory');
  if (clearBtn) clearBtn.addEventListener('click', clearHistory);
  
  // Reaction buttons
  $$('.reaction-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const reaction = btn.dataset.reaction;
      showReaction(reaction);
      playSound('pop');
    });
  });
  
  // Tab switching
  const tabSingle = $('#tabSingle');
  const tabPlaylist = $('#tabPlaylist');
  const tabTools = $('#tabTools');
  
  if (tabSingle) tabSingle.addEventListener('click', () => switchTab('single'));
  if (tabPlaylist) tabPlaylist.addEventListener('click', () => switchTab('playlist'));
  if (tabTools) tabTools.addEventListener('click', () => switchTab('tools'));
  
  // FAB quick download
  const fab = $('#fab');
  if (fab) {
    fab.addEventListener('click', () => {
      const url = $('#ytUrl').value.trim();
      if (url) {
        fetchInfo();
        playSound('click');
      } else {
        toast('⚠️ Paste a YouTube link first!', 'error');
      }
    });
  }
  
  // Override theme toggle
  const themeToggle = $('#themeToggle');
  if (themeToggle) {
    themeToggle.removeEventListener('click', () => {});
    themeToggle.addEventListener('click', toggleTheme);
  }
  
  // Social buttons
  $$('.social-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      showReaction('love');
      playSound('success');
      toast('❤️ Thank you for your support!', 'info');
    });
  });
}

// Initialize enhanced features
function initEnhanced() {
  wireEnhancedEvents();
  updateStats();
  updateProgressEmoji('idle');
  
  // Set initial theme icon
  const icon = $('#themeIcon');
  const isDark = document.documentElement.classList.contains('dark');
  if (icon) icon.textContent = isDark ? '🌙' : '☀️';
  
  // Hide empty history message if there's history
  const historyList = $('#historyList');
  const historyEmpty = $('#historyEmpty');
  if (historyList && historyEmpty) {
    historyEmpty.style.display = historyList.children.length > 0 ? 'none' : 'block';
  }
  
  console.log('🎬 TubeNova Enhanced Edition loaded!');
}

// Run on load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initEnhanced);
} else {
  initEnhanced();
}
