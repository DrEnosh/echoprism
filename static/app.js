// EchoPrism Frontend Application Logic

// Application State
const state = {
  articles: [],
  presets: [],
  selectedPresetId: null,
  availableKeywords: [],
  activeKeywords: new Set(),
  activeSignalFilter: 'ALL',
  activeView: 'briefing',
  briefings: [],
  clusters: [],
  stats: {
    total_articles: 0,
    filtered_articles: 0,
    cluster_count: 0,
    duplicates_count: 0,
    noise_reduction_pct: 0,
    reading_time_saved_min: 0
  },
  apiKey: localStorage.getItem('echoprism_api_key') || '',
  model: localStorage.getItem('echoprism_model') || 'gemini-3.8-flash',
  threshold: parseFloat(localStorage.getItem('echoprism_threshold') || '0.08')
};

// DOM Elements
const el = {
  presetsContainer: document.getElementById('preset-container'),
  keywordChipsContainer: document.getElementById('keyword-chips-container'),
  briefingsContainer: document.getElementById('briefings-container'),
  matrixContainer: document.getElementById('matrix-container'),
  rawContainer: document.getElementById('raw-container'),
  filterStatusText: document.getElementById('filter-status-text'),
  
  // Metrics
  metricIngested: document.getElementById('metric-ingested'),
  metricDevelopments: document.getElementById('metric-developments'),
  metricNoise: document.getElementById('metric-noise'),
  metricDuplicates: document.getElementById('metric-duplicates'),
  metricTime: document.getElementById('metric-time'),
  rawCountTag: document.getElementById('raw-count-tag'),

  // Buttons & Inputs
  btnProcessNow: document.getElementById('btn-process-now'),
  btnCopyBrief: document.getElementById('btn-copy-brief'),
  btnExportHtml: document.getElementById('btn-export-html'),
  btnApiSettings: document.getElementById('btn-api-settings'),
  apiStatusBadge: document.getElementById('api-status-badge'),
  
  // Tabs
  tabButtons: document.querySelectorAll('.tab-btn'),
  tabPanes: document.querySelectorAll('.tab-pane'),
  signalButtons: document.querySelectorAll('.signal-btn'),
  viewButtons: document.querySelectorAll('.view-btn'),

  // Ingestion inputs
  inputUrls: document.getElementById('input-urls'),
  btnFetchUrls: document.getElementById('btn-fetch-urls'),
  inputRss: document.getElementById('input-rss'),
  btnFetchRss: document.getElementById('btn-fetch-rss'),
  inputRaw: document.getElementById('input-raw'),
  btnFetchRaw: document.getElementById('btn-fetch-raw'),

  // Settings Modal
  settingsModal: document.getElementById('settings-modal'),
  btnCloseModal: document.getElementById('btn-close-modal'),
  inputApiKey: document.getElementById('input-api-key'),
  selectModel: document.getElementById('select-model'),
  sliderThreshold: document.getElementById('slider-threshold'),
  thresholdVal: document.getElementById('threshold-val'),
  btnSaveSettings: document.getElementById('btn-save-settings'),

  // Toast
  toast: document.getElementById('toast'),
  toastMsg: document.getElementById('toast-msg')
};

// Initialize Application
async function init() {
  updateApiBadge();
  setupEventListeners();
  await loadPresets();
  // Automatically select first preset
  if (state.presets.length > 0) {
    await selectPreset(state.presets[0].id);
  }
  lucide.createIcons();
}

function updateApiBadge() {
  if (state.apiKey && state.apiKey.trim().length > 5) {
    el.apiStatusBadge.textContent = `API: ${state.model} (Active)`;
    el.apiStatusBadge.className = 'text-cyan-400 font-semibold';
  } else {
    el.apiStatusBadge.textContent = 'Engine: Local NLP (Active)';
    el.apiStatusBadge.className = 'text-emerald-400 font-semibold';
  }
}

function showToast(message, isError = false) {
  el.toastMsg.textContent = message;
  el.toast.className = `fixed bottom-6 right-6 ${isError ? 'bg-red-950 border-red-800 text-red-200' : 'bg-slate-800 border-slate-700 text-white'} px-4 py-2.5 rounded-xl shadow-2xl text-xs font-semibold flex items-center gap-2 transform translate-y-0 opacity-100 transition-all duration-300 z-50`;
  setTimeout(() => {
    el.toast.className = 'fixed bottom-6 right-6 bg-slate-800 border-slate-700 text-white px-4 py-2.5 rounded-xl shadow-2xl text-xs font-semibold flex items-center gap-2 transform translate-y-20 opacity-0 transition-all duration-300 z-50';
  }, 3000);
}

// Preset Loader
async function loadPresets() {
  try {
    const res = await fetch('/api/presets');
    state.presets = await res.json();
    renderPresetCards();
  } catch (err) {
    console.error('Failed to load presets:', err);
    showToast('Failed to load preset datasets', true);
  }
}

function renderPresetCards() {
  el.presetsContainer.innerHTML = '';
  state.presets.forEach(p => {
    const isSelected = p.id === state.selectedPresetId;
    const card = document.createElement('div');
    card.className = `cursor-pointer p-4 rounded-xl border transition-all text-left ${
      isSelected 
        ? 'bg-cyan-950/40 border-cyan-500 shadow-lg shadow-cyan-950/30' 
        : 'bg-slate-950 border-slate-800 hover:border-slate-700 hover:bg-slate-900/50'
    }`;
    card.innerHTML = `
      <div class="flex items-center justify-between mb-2">
        <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
          isSelected ? 'bg-cyan-500 text-slate-950' : 'bg-slate-800 text-slate-400'
        }">${p.category}</span>
        <span class="text-xs font-mono text-slate-400">${p.article_count} articles</span>
      </div>
      <h4 class="text-xs font-bold text-slate-100 line-clamp-1 mb-1">${p.title}</h4>
      <p class="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">${p.description}</p>
    `;
    card.onclick = () => selectPreset(p.id);
    el.presetsContainer.appendChild(card);
  });
  lucide.createIcons();
}

async function selectPreset(presetId) {
  state.selectedPresetId = presetId;
  renderPresetCards();
  
  try {
    const res = await fetch(`/api/presets/${presetId}`);
    const data = await res.json();
    state.articles = data.articles || [];
    state.availableKeywords = data.default_keywords || [];
    state.activeKeywords.clear(); // start with all or default
    renderKeywordChips();
    updateMetrics({
      total_articles: state.articles.length,
      filtered_articles: state.articles.length,
      cluster_count: 0,
      duplicates_count: 0,
      noise_reduction_pct: 0,
      reading_time_saved_min: 0
    });
    // Auto-process the preset so the briefing is immediately visible
    await processPipeline();
  } catch (err) {
    console.error('Error fetching preset articles:', err);
    showToast('Failed to load preset articles', true);
  }
}

// Render Keywords Chips
function renderKeywordChips() {
  el.keywordChipsContainer.innerHTML = '';
  
  // "All Topics" Pill
  const allChip = document.createElement('button');
  const isAllActive = state.activeKeywords.size === 0;
  allChip.className = `chip px-3 py-1 rounded-lg text-xs font-semibold border ${
    isAllActive 
      ? 'bg-cyan-600 border-cyan-500 text-white shadow-sm shadow-cyan-500/20' 
      : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200'
  }`;
  allChip.textContent = 'All Topics';
  allChip.onclick = () => {
    state.activeKeywords.clear();
    renderKeywordChips();
    processPipeline();
  };
  el.keywordChipsContainer.appendChild(allChip);

  // Individual Keyword Chips
  state.availableKeywords.forEach(kw => {
    const isActive = state.activeKeywords.has(kw);
    const chip = document.createElement('button');
    chip.className = `chip px-2.5 py-1 rounded-lg text-xs font-medium border ${
      isActive 
        ? 'bg-cyan-600 border-cyan-500 text-white shadow-sm shadow-cyan-500/20' 
        : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
    }`;
    chip.textContent = kw;
    chip.onclick = () => {
      if (state.activeKeywords.has(kw)) {
        state.activeKeywords.delete(kw);
      } else {
        state.activeKeywords.add(kw);
      }
      renderKeywordChips();
      processPipeline();
    };
    el.keywordChipsContainer.appendChild(chip);
  });

  // Add custom keyword input
  const addContainer = document.createElement('div');
  addContainer.className = 'flex items-center gap-1';
  addContainer.innerHTML = `
    <input type="text" id="input-add-kw" placeholder="+ Add keyword" 
      class="bg-slate-950 border border-slate-800 rounded-lg px-2 py-0.5 text-xs text-slate-300 placeholder-slate-600 focus:outline-none focus:border-cyan-500 w-24">
  `;
  el.keywordChipsContainer.appendChild(addContainer);

  const addInput = document.getElementById('input-add-kw');
  addInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && addInput.value.trim()) {
      const newKw = addInput.value.trim();
      if (!state.availableKeywords.includes(newKw)) {
        state.availableKeywords.push(newKw);
        state.activeKeywords.add(newKw);
        renderKeywordChips();
        processPipeline();
      }
      addInput.value = '';
    }
  });

  el.filterStatusText.textContent = state.activeKeywords.size === 0 
    ? 'All topics active' 
    : `Filtering by: ${Array.from(state.activeKeywords).join(', ')}`;
}

// Ingestion Handlers
async function handleIngestUrls() {
  const text = el.inputUrls.value.trim();
  if (!text) {
    showToast('Please paste at least one URL', true);
    return;
  }
  const urls = text.split('\n').map(u => u.trim()).filter(Boolean);
  el.btnFetchUrls.disabled = true;
  el.btnFetchUrls.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Ingesting...';
  lucide.createIcons();

  try {
    const res = await fetch('/api/ingest/urls', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ urls })
    });
    const data = await res.json();
    if (data.articles && data.articles.length > 0) {
      state.articles = data.articles;
      state.selectedPresetId = null;
      renderPresetCards();
      extractKeywordsFromArticles();
      renderKeywordChips();
      showToast(`Successfully ingested ${data.articles.length} articles!`);
      await processPipeline();
    } else {
      showToast('Could not extract articles from the provided URLs', true);
    }
  } catch (err) {
    console.error('URL ingestion error:', err);
    showToast('Error fetching URLs. Check network connectivity.', true);
  } finally {
    el.btnFetchUrls.disabled = false;
    el.btnFetchUrls.innerHTML = '<i data-lucide="download-cloud" class="w-4 h-4"></i> Ingest URLs';
    lucide.createIcons();
  }
}

async function handleIngestRss() {
  const query = el.inputRss.value.trim();
  if (!query) {
    showToast('Please enter a search topic or RSS feed URL', true);
    return;
  }
  el.btnFetchRss.disabled = true;
  el.btnFetchRss.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Fetching...';
  lucide.createIcons();

  try {
    const res = await fetch('/api/ingest/rss', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query_or_url: query, limit: 15 })
    });
    const data = await res.json();
    if (data.articles && data.articles.length > 0) {
      state.articles = data.articles;
      state.selectedPresetId = null;
      renderPresetCards();
      extractKeywordsFromArticles();
      renderKeywordChips();
      showToast(`Fetched ${data.articles.length} stories from feed!`);
      await processPipeline();
    } else {
      showToast('No articles found for that query or feed', true);
    }
  } catch (err) {
    console.error('RSS ingestion error:', err);
    showToast('Failed to fetch RSS feed', true);
  } finally {
    el.btnFetchRss.disabled = false;
    el.btnFetchRss.innerHTML = '<i data-lucide="radio" class="w-4 h-4"></i> Fetch News Feed';
    lucide.createIcons();
  }
}

async function handleIngestRaw() {
  const text = el.inputRaw.value.trim();
  if (!text) {
    showToast('Please paste some text or newsletter content', true);
    return;
  }
  el.btnFetchRaw.disabled = true;
  el.btnFetchRaw.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Parsing...';
  lucide.createIcons();

  try {
    const res = await fetch('/api/ingest/raw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_text: text })
    });
    const data = await res.json();
    if (data.articles && data.articles.length > 0) {
      state.articles = data.articles;
      state.selectedPresetId = null;
      renderPresetCards();
      extractKeywordsFromArticles();
      renderKeywordChips();
      showToast(`Parsed ${data.articles.length} items from text!`);
      await processPipeline();
    } else {
      showToast('Could not extract articles from pasted text', true);
    }
  } catch (err) {
    console.error('Raw text parsing error:', err);
    showToast('Failed to parse text', true);
  } finally {
    el.btnFetchRaw.disabled = false;
    el.btnFetchRaw.innerHTML = '<i data-lucide="file-text" class="w-4 h-4"></i> Parse Text Articles';
    lucide.createIcons();
  }
}

function extractKeywordsFromArticles() {
  const wordsCount = {};
  const stop = new Set(['the', 'and', 'with', 'from', 'this', 'that', 'were', 'have', 'said', 'will', 'about', 'after', 'into', 'over', 'more', 'also', 'news', 'update', 'article']);
  state.articles.forEach(a => {
    const text = `${a.title || ''} ${a.content || ''}`.toLowerCase();
    const tokens = text.match(/\b[a-z0-9\-_]{4,}\b/g) || [];
    tokens.forEach(t => {
      if (!stop.has(t) && isNaN(t)) {
        wordsCount[t] = (wordsCount[t] || 0) + 1;
      }
    });
  });
  const sorted = Object.entries(wordsCount).sort((a, b) => b[1] - a[1]).slice(0, 8);
  state.availableKeywords = sorted.map(pair => pair[0]);
  state.activeKeywords.clear();
}

// Pipeline Processing (Clustering + Deduplication + Summarization)
async function processPipeline() {
  if (state.articles.length === 0) {
    showToast('No articles available to process', true);
    return;
  }

  el.btnProcessNow.disabled = true;
  el.btnProcessNow.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Synthesizing Signal...';
  lucide.createIcons();

  try {
    const payload = {
      articles: state.articles,
      keywords: state.activeKeywords.size > 0 ? Array.from(state.activeKeywords) : null,
      similarity_threshold: state.threshold,
      duplicate_threshold: 0.65,
      api_key: state.apiKey || null,
      model: state.model
    };

    const res = await fetch('/api/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Pipeline processing failed');
    }

    const data = await res.json();
    state.briefings = data.briefings || [];
    state.clusters = data.clusters || [];
    state.stats = data.stats || {};

    updateMetrics(state.stats);
    renderActiveView();
  } catch (err) {
    console.error('Processing error:', err);
    showToast(`Error: ${err.message}`, true);
  } finally {
    el.btnProcessNow.disabled = false;
    el.btnProcessNow.innerHTML = '<i data-lucide="zap" class="w-4 h-4"></i> Eliminate Overload & Generate Brief';
    lucide.createIcons();
  }
}

// Metrics Updating
function updateMetrics(stats) {
  el.metricIngested.textContent = stats.filtered_articles ?? state.articles.length;
  el.metricDevelopments.textContent = stats.cluster_count ?? 0;
  el.metricNoise.textContent = `${stats.noise_reduction_pct ?? 0}%`;
  el.metricDuplicates.textContent = `${stats.duplicates_count ?? 0} redundant syndications purged`;
  el.metricTime.textContent = `${stats.reading_time_saved_min ?? 0}m`;
  el.rawCountTag.textContent = state.articles.length;
}

// Active View Routing
function renderActiveView() {
  if (state.activeView === 'briefing') {
    el.briefingsContainer.classList.remove('hidden');
    el.matrixContainer.classList.add('hidden');
    el.rawContainer.classList.add('hidden');
    renderBriefings();
  } else if (state.activeView === 'matrix') {
    el.briefingsContainer.classList.add('hidden');
    el.matrixContainer.classList.remove('hidden');
    el.rawContainer.classList.add('hidden');
    renderClusterMatrix();
  } else if (state.activeView === 'raw') {
    el.briefingsContainer.classList.add('hidden');
    el.matrixContainer.classList.add('hidden');
    el.rawContainer.classList.remove('hidden');
    renderRawArticles();
  }
}

// Render Briefings
function renderBriefings() {
  el.briefingsContainer.innerHTML = '';
  
  const filtered = state.briefings.filter(b => {
    if (state.activeSignalFilter === 'ALL') return true;
    return b.signal_level === state.activeSignalFilter;
  });

  if (filtered.length === 0) {
    el.briefingsContainer.innerHTML = `
      <div class="bg-slate-900/40 border border-slate-800 rounded-2xl p-12 text-center text-slate-400">
        <i data-lucide="info" class="w-8 h-8 text-slate-500 mx-auto mb-3"></i>
        <h3 class="text-sm font-semibold text-slate-300">No developments match the current signal filter</h3>
        <p class="text-xs text-slate-500 mt-1">Try switching to 'All' signal priorities or clearing keyword filters.</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  filtered.forEach((b, idx) => {
    const signal = b.signal_level || 'MEDIUM';
    const badgeClass = signal === 'HIGH' ? 'badge-high' : (signal === 'MEDIUM' ? 'badge-medium' : 'badge-low');
    const badgeIcon = signal === 'HIGH' ? 'alert-triangle' : (signal === 'MEDIUM' ? 'trending-up' : 'info');

    const card = document.createElement('div');
    card.className = 'bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md brief-card-hover animate-fade-in space-y-4';

    // Source links items
    const sourceLinksHtml = (b.sources || []).map(s => `
      <li class="flex items-center justify-between text-xs py-1 border-b border-slate-800/60 last:border-0">
        <div class="flex items-center gap-2 truncate pr-2">
          <i data-lucide="external-link" class="w-3.5 h-3.5 text-cyan-400 shrink-0"></i>
          <a href="${s.url || '#'}" target="_blank" rel="noopener noreferrer" class="text-cyan-400 hover:text-cyan-300 hover:underline truncate">
            <span class="font-bold text-slate-200">[${s.source}]</span> ${s.title}
          </a>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          ${s.is_duplicate ? '<span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full border border-slate-700">Syndicated Wire</span>' : '<span class="text-[10px] bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 px-2 py-0.5 rounded-full">Unique Angle</span>'}
          <span class="text-[10px] text-slate-400 font-mono">${s.date || ''}</span>
        </div>
      </li>
    `).join('');

    // Cross-outlet framing items
    const framingHtml = (b.cross_outlet_framing || []).map(f => `
      <div class="bg-slate-950/80 border border-slate-800/80 rounded-xl p-3 text-xs space-y-1">
        <div class="flex items-center justify-between">
          <span class="font-bold text-cyan-400">${f.source}</span>
          <span class="text-[10px] text-slate-400 italic truncate max-w-[280px]">"${f.headline}"</span>
        </div>
        <p class="text-slate-300 leading-relaxed">${f.framing}</p>
      </div>
    `).join('');

    // Key quotes
    const quotesHtml = (b.key_quotes || []).map(q => `
      <blockquote class="border-l-2 border-indigo-500 pl-3 py-1 text-xs italic text-slate-300">
        "${q.quote}" &mdash; <strong class="text-indigo-400 not-italic">${q.attribution}</strong>
      </blockquote>
    `).join('');

    card.innerHTML = `
      <!-- Card Header -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800">
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 rounded-full text-[11px] font-extrabold uppercase tracking-wider flex items-center gap-1.5 ${badgeClass}">
            <i data-lucide="${badgeIcon}" class="w-3.5 h-3.5"></i>
            ${signal} SIGNAL
          </span>
          <span class="text-xs text-slate-400 font-mono">Development #${idx + 1}</span>
        </div>
        <div class="text-xs text-slate-400 flex items-center gap-3">
          <span>${b.stats?.total_articles || 0} articles grouped</span>
          <span class="text-emerald-400 font-semibold">${b.stats?.duplicate_count || 0} duplicates purged</span>
        </div>
      </div>

      <!-- Headline & Materiality Rationale -->
      <div>
        <h3 class="text-lg font-bold text-white tracking-tight leading-snug">${b.headline}</h3>
        <p class="text-xs text-slate-400 mt-1 flex items-center gap-1.5">
          <span class="text-slate-400 font-semibold uppercase text-[10px] tracking-wider">Materiality:</span>
          <span>${b.signal_rationale}</span>
        </p>
      </div>

      <!-- Executive Takeaway Banner -->
      <div class="bg-gradient-to-r from-cyan-950/50 to-slate-900 border border-cyan-800/50 rounded-xl p-3.5 text-xs text-cyan-200 leading-relaxed shadow-sm">
        <strong class="text-cyan-400 block mb-1 uppercase tracking-wider text-[10px] font-bold">Executive TL;DR</strong>
        ${b.executive_summary}
      </div>

      <!-- What Happened & Why it matters Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="bg-slate-950/50 border border-slate-800/80 rounded-xl p-3.5 space-y-2">
          <h4 class="font-bold text-slate-300 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="check-square" class="w-3.5 h-3.5 text-cyan-400"></i>
            What Happened (Verified Facts)
          </h4>
          <ul class="space-y-1.5 text-slate-300">
            ${(b.what_happened || []).map(fact => `<li class="flex items-start gap-1.5"><span class="text-cyan-500 font-bold">&bull;</span><span>${fact}</span></li>`).join('')}
          </ul>
        </div>

        <div class="bg-slate-950/50 border border-slate-800/80 rounded-xl p-3.5 space-y-2">
          <h4 class="font-bold text-slate-300 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="compass" class="w-3.5 h-3.5 text-indigo-400"></i>
            Why It Matters (PR & Strategic Angle)
          </h4>
          <p class="text-slate-300 leading-relaxed">${b.why_it_matters}</p>
        </div>
      </div>

      <!-- Cross-Outlet Framing -->
      ${framingHtml ? `
        <div class="space-y-2">
          <h4 class="font-bold text-slate-300 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="split" class="w-3.5 h-3.5 text-cyan-400"></i>
            Cross-Outlet Framing & Narrative Divergence
          </h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            ${framingHtml}
          </div>
        </div>
      ` : ''}

      <!-- Quotes -->
      ${quotesHtml ? `
        <div class="space-y-2 bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
          <h4 class="font-bold text-slate-300 text-[11px] uppercase tracking-wider flex items-center gap-1.5">
            <i data-lucide="quote" class="w-3.5 h-3.5 text-indigo-400"></i>
            Key Stakeholder Quotes
          </h4>
          <div class="space-y-2">
            ${quotesHtml}
          </div>
        </div>
      ` : ''}

      <!-- Action Recommendation -->
      ${b.recommended_action ? `
        <div class="bg-amber-950/30 border border-amber-800/40 rounded-xl p-3 text-xs text-amber-200 flex items-start gap-2.5">
          <i data-lucide="target" class="w-4 h-4 text-amber-400 shrink-0 mt-0.5"></i>
          <div>
            <strong class="text-amber-400 uppercase text-[10px] tracking-wider block font-bold">Recommended Comms Action:</strong>
            ${b.recommended_action}
          </div>
        </div>
      ` : ''}

      <!-- Collapsible Verified Source Links -->
      <details class="bg-slate-950/60 border border-slate-800 rounded-xl p-3 text-xs group">
        <summary class="font-bold text-slate-300 cursor-pointer flex items-center justify-between select-none">
          <span class="flex items-center gap-2">
            <i data-lucide="link" class="w-3.5 h-3.5 text-cyan-400"></i>
            Verified Sources & Coverage Breakdown (${(b.sources || []).length} outlets)
          </span>
          <span class="text-[11px] text-cyan-400 group-open:rotate-180 transition-transform">▼</span>
        </summary>
        <ul class="mt-3 space-y-1">
          ${sourceLinksHtml}
        </ul>
      </details>
    `;

    el.briefingsContainer.appendChild(card);
  });

  lucide.createIcons();
}

// Render Cluster Tree Matrix
function renderClusterMatrix() {
  el.matrixContainer.innerHTML = '';
  
  if (state.clusters.length === 0) {
    el.matrixContainer.innerHTML = '<div class="text-center p-8 text-slate-500 text-xs">No clusters generated yet.</div>';
    return;
  }

  state.clusters.forEach((c, idx) => {
    const card = document.createElement('div');
    card.className = 'bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3';
    
    const uniqueList = (c.unique_angles || []).map(a => `
      <div class="bg-slate-950 p-2.5 rounded-lg border border-slate-800 text-xs space-y-1">
        <div class="flex items-center justify-between">
          <span class="font-bold text-cyan-400">${a.source}</span>
          <span class="text-[10px] text-slate-400">${a.date || ''}</span>
        </div>
        <p class="text-slate-200">${a.title}</p>
      </div>
    `).join('');

    const duplicateList = (c.duplicate_coverage || []).map(d => `
      <div class="bg-slate-950/50 p-2 rounded-lg border border-slate-800/60 text-[11px] flex items-center justify-between">
        <span class="font-medium text-slate-400">[${d.source}] ${d.title}</span>
        <span class="text-[10px] text-red-400/80 bg-red-950/40 px-2 py-0.5 rounded border border-red-900/40">Duplicate Purged</span>
      </div>
    `).join('');

    card.innerHTML = `
      <div class="flex items-center justify-between pb-2 border-b border-slate-800">
        <h4 class="text-sm font-bold text-white flex items-center gap-2">
          <i data-lucide="git-commit" class="w-4 h-4 text-cyan-400"></i>
          Cluster #${idx + 1}: ${c.headline}
        </h4>
        <span class="text-xs font-mono text-cyan-400 font-bold">${c.articles_count} Articles Total</span>
      </div>

      <!-- Keywords Tags -->
      <div class="flex items-center gap-1.5 flex-wrap">
        <span class="text-[10px] font-bold text-slate-400 uppercase">Top Terms:</span>
        ${(c.top_keywords || []).map(kw => `<span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded-md">${kw}</span>`).join('')}
      </div>

      <!-- Primary Anchor -->
      <div class="bg-cyan-950/30 border border-cyan-800/60 rounded-xl p-3 text-xs">
        <div class="flex items-center justify-between text-[11px] mb-1">
          <span class="font-bold uppercase tracking-wider text-cyan-400">Primary Story Anchor</span>
          <span class="text-slate-400">${c.anchor_article?.source}</span>
        </div>
        <p class="font-semibold text-slate-100">${c.anchor_article?.title}</p>
      </div>

      <!-- Unique Angles Column -->
      <div class="space-y-1.5">
        <h5 class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Unique Reporting Perspectives (${c.unique_angles?.length || 0})</h5>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          ${uniqueList}
        </div>
      </div>

      <!-- Duplicate Coverage Column -->
      ${c.duplicate_coverage && c.duplicate_coverage.length > 0 ? `
        <div class="space-y-1.5 pt-2 border-t border-slate-800/60">
          <h5 class="text-[11px] font-bold uppercase tracking-wider text-red-400/80">
            Syndicated Reposts & Redundant Noise Purged (${c.duplicate_coverage.length})
          </h5>
          <div class="space-y-1">
            ${duplicateList}
          </div>
        </div>
      ` : ''}
    `;

    el.matrixContainer.appendChild(card);
  });

  lucide.createIcons();
}

// Render Raw Ingested Articles
function renderRawArticles() {
  el.rawContainer.innerHTML = '';
  if (state.articles.length === 0) {
    el.rawContainer.innerHTML = '<div class="text-center p-8 text-slate-500 text-xs">No articles ingested.</div>';
    return;
  }

  state.articles.forEach((art, idx) => {
    const card = document.createElement('div');
    card.className = 'bg-slate-900/60 border border-slate-800 rounded-xl p-4 text-xs space-y-2';
    card.innerHTML = `
      <div class="flex items-center justify-between">
        <span class="font-bold text-cyan-400">[${art.source || 'Unknown'}]</span>
        <span class="text-slate-400 font-mono text-[10px]">${art.date || ''}</span>
      </div>
      <h4 class="font-bold text-slate-100 text-sm">${art.title}</h4>
      <p class="text-slate-400 line-clamp-3 leading-relaxed">${art.content}</p>
      ${art.url ? `<a href="${art.url}" target="_blank" class="text-cyan-400 hover:underline text-[11px] flex items-center gap-1"><i data-lucide="external-link" class="w-3 h-3"></i> ${art.url}</a>` : ''}
    `;
    el.rawContainer.appendChild(card);
  });

  lucide.createIcons();
}

// Export Handlers
async function handleCopyBrief() {
  if (state.briefings.length === 0) {
    showToast('Generate a briefing first before copying', true);
    return;
  }

  try {
    const res = await fetch('/api/export/markdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        briefings: state.briefings,
        stats: state.stats,
        title: state.selectedPresetId 
          ? state.presets.find(p => p.id === state.selectedPresetId)?.title 
          : 'Executive PR Briefing'
      })
    });
    const data = await res.json();
    await navigator.clipboard.writeText(data.markdown);
    showToast('PR Briefing copied to clipboard (Markdown)!');
  } catch (err) {
    console.error('Clipboard copy error:', err);
    showToast('Failed to copy briefing', true);
  }
}

async function handleExportHtml() {
  if (state.briefings.length === 0) {
    showToast('Generate a briefing first before exporting', true);
    return;
  }

  try {
    const res = await fetch('/api/export/html', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        briefings: state.briefings,
        stats: state.stats,
        title: state.selectedPresetId 
          ? state.presets.find(p => p.id === state.selectedPresetId)?.title 
          : 'Executive PR Briefing'
      })
    });
    const data = await res.json();
    const blob = new Blob([data.html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Executive_PR_Briefing_${new Date().toISOString().slice(0, 10)}.html`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('HTML Report downloaded successfully!');
  } catch (err) {
    console.error('HTML export error:', err);
    showToast('Failed to export HTML', true);
  }
}

// Event Listeners Setup
function setupEventListeners() {
  // Tabs Switcher (Ingestion)
  el.tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;
      el.tabButtons.forEach(b => b.classList.remove('active', 'bg-slate-800', 'text-white'));
      btn.classList.add('active', 'bg-slate-800', 'text-white');
      el.tabPanes.forEach(p => p.classList.add('hidden'));
      document.getElementById(`tab-${target}`).classList.remove('hidden');
    });
  });

  // Signal Priority Filter Buttons
  el.signalButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      el.signalButtons.forEach(b => b.classList.remove('active', 'bg-slate-800', 'text-white'));
      btn.classList.add('active', 'bg-slate-800', 'text-white');
      state.activeSignalFilter = btn.dataset.signal;
      renderBriefings();
    });
  });

  // View Switcher Buttons
  el.viewButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      el.viewButtons.forEach(b => b.classList.remove('active', 'bg-slate-800', 'text-white'));
      btn.classList.add('active', 'bg-slate-800', 'text-white');
      state.activeView = btn.dataset.view;
      renderActiveView();
    });
  });

  // Ingestion Action Buttons
  el.btnFetchUrls.addEventListener('click', handleIngestUrls);
  el.btnFetchRss.addEventListener('click', handleIngestRss);
  el.btnFetchRaw.addEventListener('click', handleIngestRaw);
  el.btnProcessNow.addEventListener('click', processPipeline);

  // Copy & Export
  el.btnCopyBrief.addEventListener('click', handleCopyBrief);
  el.btnExportHtml.addEventListener('click', handleExportHtml);

  // Settings Modal
  el.btnApiSettings.addEventListener('click', () => {
    el.inputApiKey.value = state.apiKey;
    el.selectModel.value = state.model;
    el.sliderThreshold.value = state.threshold;
    el.thresholdVal.textContent = state.threshold;
    el.settingsModal.classList.remove('hidden');
  });

  el.btnCloseModal.addEventListener('click', () => {
    el.settingsModal.classList.add('hidden');
  });

  el.sliderThreshold.addEventListener('input', (e) => {
    el.thresholdVal.textContent = e.target.value;
  });

  el.btnSaveSettings.addEventListener('click', () => {
    state.apiKey = el.inputApiKey.value.trim();
    state.model = el.selectModel.value;
    state.threshold = parseFloat(el.sliderThreshold.value);

    localStorage.setItem('echoprism_api_key', state.apiKey);
    localStorage.setItem('echoprism_model', state.model);
    localStorage.setItem('echoprism_threshold', state.threshold.toString());

    updateApiBadge();
    el.settingsModal.classList.add('hidden');
    showToast('Settings saved successfully!');
    processPipeline();
  });
}

// Run on page load
document.addEventListener('DOMContentLoaded', init);
