// TubeNova Serverless Fallback
// Client-side YouTube info extraction using CORS proxies

const CORS_PROXIES = [
  'https://corsproxy.io/?',
  'https://api.allorigins.win/raw?url=',
  'https://cors-anywhere.herokuapp.com/'
];

let currentProxyIndex = 0;

// Get current CORS proxy
function getCorsProxy() {
  return CORS_PROXIES[currentProxyIndex % CORS_PROXIES.length];
}

// Rotate to next proxy on failure
function rotateProxy() {
  currentProxyIndex++;
  console.log('🔄 Switching to proxy:', getCorsProxy());
}

// Extract video ID from YouTube URL
function extractVideoId(url) {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\?\/]+)/,
    /youtube\.com\/shorts\/([^&\?\/]+)/
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return null;
}

// Fetch video info using CORS proxy fallback
async function fetchInfoFallback(url) {
  const videoId = extractVideoId(url);
  if (!videoId) {
    throw new Error('Invalid YouTube URL');
  }
  
  // Try oEmbed API first (no CORS issues)
  try {
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const response = await fetch(oembedUrl);
    
    if (response.ok) {
      const data = await response.json();
      
      // Get additional info from noembed.com (more detailed)
      let duration = 0;
      try {
        const noembedUrl = `https://noembed.com/embed?url=https://www.youtube.com/watch?v=${videoId}`;
        const noembedRes = await fetch(noembedUrl);
        if (noembedRes.ok) {
          const noembedData = await noembedRes.json();
          duration = noembedData.duration || 0;
        }
      } catch {}
      
      return {
        success: true,
        data: {
          id: videoId,
          title: data.title,
          uploader: data.author_name,
          thumbnail: data.thumbnail_url,
          duration: duration,
          webpage_url: `https://www.youtube.com/watch?v=${videoId}`,
          formats: generateMockFormats(videoId)
        }
      };
    }
  } catch (e) {
    console.warn('oEmbed failed:', e);
  }
  
  // Fallback to scraping with CORS proxy
  return await scrapeVideoInfo(videoId);
}

// Generate mock formats (best effort without backend)
function generateMockFormats(videoId) {
  const qualities = [
    { quality: '144p', height: 144, format_note: 'Tiny 🐜', ext: 'mp4', filesize: 5 * 1024 * 1024 },
    { quality: '360p', height: 360, format_note: 'Low 📱', ext: 'mp4', filesize: 15 * 1024 * 1024 },
    { quality: '480p', height: 480, format_note: 'Good 👌', ext: 'mp4', filesize: 30 * 1024 * 1024 },
    { quality: '720p', height: 720, format_note: 'HD 📺', ext: 'mp4', filesize: 70 * 1024 * 1024 },
    { quality: '1080p', height: 1080, format_note: 'Full HD 🌟', ext: 'mp4', filesize: 150 * 1024 * 1024 }
  ];
  
  const audioFormats = [
    { quality: 'audio_128k', format_note: 'Audio 128k 🎵', ext: 'm4a', acodec: 'mp4a', abr: 128 },
    { quality: 'audio_320k', format_note: 'Audio 320k 🎧', ext: 'm4a', acodec: 'mp4a', abr: 320 }
  ];
  
  return [...qualities, ...audioFormats].map((fmt, idx) => ({
    format_id: `mock_${idx}`,
    ...fmt,
    url: `https://www.youtube.com/watch?v=${videoId}` // Placeholder
  }));
}

// Scrape video info using CORS proxy
async function scrapeVideoInfo(videoId) {
  const watchUrl = `https://www.youtube.com/watch?v=${videoId}`;
  const proxy = getCorsProxy();
  
  try {
    const response = await fetch(proxy + encodeURIComponent(watchUrl));
    const html = await response.text();
    
    // Parse title
    const titleMatch = html.match(/<title>([^<]+)<\/title>/);
    const title = titleMatch ? titleMatch[1].replace(' - YouTube', '') : 'Unknown Title';
    
    // Parse channel name
    const channelMatch = html.match(/"author":"([^"]+)"/);
    const uploader = channelMatch ? channelMatch[1] : 'Unknown Channel';
    
    // Parse thumbnail
    const thumbnail = `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`;
    
    // Parse duration from meta tags
    let duration = 0;
    const durationMatch = html.match(/"lengthSeconds":"(\d+)"/);
    if (durationMatch) {
      duration = parseInt(durationMatch[1]);
    }
    
    return {
      success: true,
      data: {
        id: videoId,
        title: title,
        uploader: uploader,
        thumbnail: thumbnail,
        duration: duration,
        webpage_url: watchUrl,
        formats: generateMockFormats(videoId)
      }
    };
  } catch (error) {
    console.error('Scraping failed with proxy:', proxy, error);
    rotateProxy();
    
    if (currentProxyIndex < CORS_PROXIES.length * 2) {
      // Try next proxy
      return scrapeVideoInfo(videoId);
    }
    
    throw new Error('All CORS proxies failed');
  }
}

// Download video using redirect (opens in new tab)
function downloadFallback(url, quality, format) {
  const videoId = extractVideoId(url);
  if (!videoId) {
    throw new Error('Invalid YouTube URL');
  }
  
  // Use third-party download services
  const services = [
    `https://ytmp3.nu/api/download?url=https://www.youtube.com/watch?v=${videoId}`,
    `https://yt5s.com/api/ajaxSearch/index?url=https://www.youtube.com/watch?v=${videoId}`,
    `https://ssyoutube.com/watch?v=${videoId}` // Just prepend 'ss' to youtube.com
  ];
  
  // Open first service in new tab
  window.open(services[2], '_blank');
  
  toast('🌐 Opening download service...', 'info');
  toast('⚠️ For direct downloads, configure a backend server!', 'info');
}

// Check if backend is available
async function checkBackendAvailability(backendUrl) {
  if (!backendUrl) return false;
  
  try {
    const response = await fetch(`${backendUrl}/api/health`, {
      method: 'GET',
      mode: 'cors',
      cache: 'no-cache'
    });
    return response.ok;
  } catch {
    return false;
  }
}

// Auto-detect and use fallback if needed
async function smartFetch(url) {
  const backendUrl = BACKEND();
  
  // Try backend first
  if (backendUrl) {
    const isAvailable = await checkBackendAvailability(backendUrl);
    if (isAvailable) {
      try {
        const response = await fetch(`${backendUrl}/api/info`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url })
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            console.log('✅ Using backend server');
            return { mode: 'backend', data: data };
          }
        }
      } catch (e) {
        console.warn('Backend failed:', e);
      }
    }
  }
  
  // Fallback to client-side
  console.log('🌐 Using serverless fallback');
  toast('ℹ️ Using client-side mode (limited features)', 'info');
  const fallbackData = await fetchInfoFallback(url);
  return { mode: 'fallback', data: fallbackData };
}

// Export functions
window.TubeNovaFallback = {
  smartFetch,
  downloadFallback,
  checkBackendAvailability,
  extractVideoId
};

console.log('🚀 TubeNova Fallback loaded (Serverless mode available)');
