// TubeNova Serverless Fallback
// Client-side YouTube info extraction using Invidious API

const CORS_PROXIES = [
  'https://corsproxy.io/?',
  'https://api.allorigins.win/raw?url=',
  'https://cors-anywhere.herokuapp.com/'
];

let currentProxyIndex = 0;

// Backend URL helper (matches app.js)
const BACKEND = () => (window.BACKEND_URL || 'http://127.0.0.1:5000').replace(/\/$/, '');

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

// Fetch video info using multiple APIs
async function fetchInfoFallback(url) {
  const videoId = extractVideoId(url);
  if (!videoId) {
    throw new Error('Invalid YouTube URL');
  }
  
  // Try Invidious API (best option - no CORS, full data)
  const invidiousInstances = [
    'https://invidious.io.lol',
    'https://inv.nadeko.net',
    'https://invidious.private.coffee'
  ];
  
  for (const instance of invidiousInstances) {
    try {
      const response = await fetch(`${instance}/api/v1/videos/${videoId}`);
      if (response.ok) {
        const data = await response.json();
        
        // Parse formats from Invidious
        const formats = [];
        
        // Add video formats
        if (data.formatStreams) {
          data.formatStreams.forEach(f => {
            if (f.type && f.type.includes('video')) {
              const quality = f.qualityLabel || f.quality || `${f.resolution}p`;
              formats.push({
                format_id: f.itag || f.url,
                quality: quality,
                height: parseInt(f.resolution) || 0,
                format_note: quality,
                ext: f.container || 'mp4',
                filesize: f.size || 0,
                url: f.url,
                type: 'video'
              });
            }
          });
        }
        
        // Add adaptive formats (higher quality)
        if (data.adaptiveFormats) {
          data.adaptiveFormats.forEach(f => {
            if (f.type && f.type.includes('video')) {
              const quality = f.qualityLabel || f.quality || `${f.resolution}p`;
              formats.push({
                format_id: f.itag || f.url,
                quality: quality,
                height: parseInt(f.resolution) || 0,
                format_note: quality,
                ext: f.container || 'mp4',
                filesize: f.size || 0,
                url: f.url,
                type: 'video'
              });
            } else if (f.type && f.type.includes('audio')) {
              const bitrate = f.bitrate ? Math.round(f.bitrate / 1000) + 'k' : '128k';
              formats.push({
                format_id: f.itag || f.url,
                quality: bitrate,
                format_note: `Audio ${bitrate}`,
                ext: f.container || 'm4a',
                acodec: f.audioCodec || 'mp4a',
                abr: parseInt(bitrate),
                filesize: f.size || 0,
                url: f.url,
                type: 'audio'
              });
            }
          });
        }
        
        return {
          success: true,
          data: {
            id: videoId,
            title: data.title,
            uploader: data.author,
            thumbnail: data.videoThumbnails?.[0]?.url || `https://i.ytimg.com/vi/${videoId}/maxresdefault.jpg`,
            duration: data.lengthSeconds || 0,
            webpage_url: `https://www.youtube.com/watch?v=${videoId}`,
            formats: formats
          }
        };
      }
    } catch (e) {
      console.warn(`Invidious ${instance} failed:`, e);
      continue;
    }
  }
  
  // Fallback to oEmbed API (basic info only)
  try {
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const response = await fetch(oembedUrl);
    
    if (response.ok) {
      const data = await response.json();
      
      return {
        success: true,
        data: {
          id: videoId,
          title: data.title,
          uploader: data.author_name,
          thumbnail: data.thumbnail_url,
          duration: 0,
          webpage_url: `https://www.youtube.com/watch?v=${videoId}`,
          formats: generateMockFormats(videoId)
        }
      };
    }
  } catch (e) {
    console.warn('oEmbed failed:', e);
  }
  
  throw new Error('All fallback methods failed');
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

// Download video using direct URL from Invidious
async function downloadFallback(videoInfo, quality, type) {
  try {
    // Find the matching format from fetched info
    const formats = videoInfo.formats || [];
    let selectedFormat = null;
    
    if (type === 'video') {
      // Find video format matching quality
      selectedFormat = formats.find(f => 
        f.type === 'video' && f.quality && f.quality.includes(quality)
      );
      // Fallback to closest quality
      if (!selectedFormat) {
        selectedFormat = formats.find(f => f.type === 'video' && f.url);
      }
    } else {
      // Audio format
      selectedFormat = formats.find(f => 
        f.type === 'audio' && f.quality && f.quality.includes(quality)
      );
      if (!selectedFormat) {
        selectedFormat = formats.find(f => f.type === 'audio' && f.url);
      }
    }
    
    if (selectedFormat && selectedFormat.url) {
      // Direct download using URL
      const a = document.createElement('a');
      a.href = selectedFormat.url;
      const safeTitle = (videoInfo.title || 'tubenova').replace(/[^\w\-\s\(\)\[\]]+/g, '_').slice(0, 80);
      const ext = selectedFormat.ext || (type === 'audio' ? 'm4a' : 'mp4');
      a.download = `${safeTitle}_${quality}.${ext}`;
      a.target = '_blank';
      document.body.appendChild(a);
      a.click();
      a.remove();
      
      return true;
    } else {
      // Fallback to third-party service
      const videoId = extractVideoId(videoInfo.webpage_url);
      const service = `https://ssyoutube.com/watch?v=${videoId}`;
      window.open(service, '_blank');
      
      toast('🌐 Opening download service...', 'info');
      toast('⚠️ For best results, configure a backend server!', 'info');
      return false;
    }
  } catch (e) {
    console.error('Download fallback error:', e);
    toast('❌ Download failed', 'error');
    return false;
  }
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
        const response = await fetch(`${backendUrl}/api/info?url=${encodeURIComponent(url)}`);
        
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
  extractVideoId,
  fetchInfoFallback
};

console.log('🚀 TubeNova Fallback loaded (Serverless mode with Invidious API)');
