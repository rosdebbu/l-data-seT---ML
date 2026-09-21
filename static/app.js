/**
 * Crop & Fertilizer ML — Client Application Script
 * Orchestrates real-time ML predictions, dual-synced inputs,
 * immediate inline results, Soil Health Card generation,
 * model performance benchmarks, and interactive dataset explorer.
 */

// ============================================================
// TAB NAVIGATION (5 Core Features)
// ============================================================
function switchTab(tabKey) {
  const tabs = ['crop', 'fertilizer', 'geo', 'analytics', 'report', 'data'];
  
  tabs.forEach(t => {
    const view = document.getElementById(`view-${t}`);
    const btn = document.getElementById(`tab-btn-${t}`);
    
    if (t === tabKey) {
      if (view) view.classList.remove('hidden');
      if (btn) {
        btn.classList.add('bg-almond', 'text-eclipse', 'font-bold', 'shadow-almond-glow');
        btn.classList.remove('text-almond/80');
      }
    } else {
      if (view) view.classList.add('hidden');
      if (btn) {
        btn.classList.remove('bg-almond', 'text-eclipse', 'font-bold', 'shadow-almond-glow');
        btn.classList.add('text-almond/80');
      }
    }
  });

  if (tabKey === 'geo') {
    if (!geoMap) {
      setTimeout(() => initSatelliteMap(), 50);
    } else {
      setTimeout(() => { if (geoMap) geoMap.invalidateSize(); }, 150);
    }
  } else if (tabKey === 'report') {
    syncSoilReport();
  } else if (tabKey === 'data') {
    if (!currentDatasetData || currentDatasetData.length === 0) {
      loadDatasetExplorer('crop');
    }
  }

  // Re-initialize Lucide icons when views become visible
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

// ============================================================
// DUAL SYNCED INPUTS & DEBOUNCED LIVE INFERENCE
// ============================================================
let cropDebounceTimer = null;
let fertDebounceTimer = null;

function debouncedCropPredict() {
  clearTimeout(cropDebounceTimer);
  cropDebounceTimer = setTimeout(() => {
    executeCropPrediction(true);
  }, 120);
}

function debouncedFertPredict() {
  clearTimeout(fertDebounceTimer);
  fertDebounceTimer = setTimeout(() => {
    executeFertPrediction(true);
  }, 120);
}

function syncCropSlider(key, val) {
  const numInput = document.getElementById(`crop-num-${key}`);
  if (numInput) numInput.value = val;
  debouncedCropPredict();
}

function syncCropInput(key, val) {
  const slider = document.getElementById(`crop-in-${key}`);
  if (slider) slider.value = val;
  debouncedCropPredict();
}

function syncFertSlider(key, val) {
  const numInput = document.getElementById(`fert-num-${key}`);
  if (numInput) numInput.value = val;
  debouncedFertPredict();
}

function syncFertInput(key, val) {
  const slider = document.getElementById(`fert-in-${key}`);
  if (slider) slider.value = val;
  debouncedFertPredict();
}

// Global cache of latest results for Soil Health Card
let latestCropData = null;
let latestFertData = null;

// ============================================================
// CROP PRESETS & INFERENCE
// ============================================================
const CROP_PRESETS = {
  rice: { N: 90, P: 45, K: 40, temperature: 26.0, humidity: 82, ph: 6.5, rainfall: 240 },
  chickpea: { N: 30, P: 65, K: 45, temperature: 18.5, humidity: 45, ph: 7.2, rainfall: 65 },
  maize: { N: 75, P: 42, K: 25, temperature: 24.0, humidity: 62, ph: 6.2, rainfall: 95 },
  mothbeans: { N: 22, P: 40, K: 20, temperature: 31.0, humidity: 35, ph: 7.8, rainfall: 42 }
};

function loadCropPreset(name) {
  const p = CROP_PRESETS[name];
  if (!p) return;

  const setVal = (key, val) => {
    const s = document.getElementById(`crop-in-${key}`);
    const n = document.getElementById(`crop-num-${key}`);
    if (s) s.value = val;
    if (n) n.value = val;
  };

  setVal('N', p.N);
  setVal('P', p.P);
  setVal('K', p.K);
  setVal('temperature', p.temperature);
  setVal('humidity', p.humidity);
  setVal('ph', p.ph);
  setVal('rainfall', p.rainfall);

  executeCropPrediction(false);
}

async function handleCropPredict(e) {
  if (e) e.preventDefault();
  await executeCropPrediction(false);
}

async function executeCropPrediction(isSilent = false) {
  const submitBtn = document.getElementById('crop-submit-btn');
  const originalText = submitBtn ? submitBtn.innerHTML : '';
  
  if (!isSilent && submitBtn) {
    submitBtn.innerHTML = `<span class="inline-block animate-spin mr-2">⏳</span> Computing Crop Recommendation...`;
    submitBtn.disabled = true;
  }

  const payload = {
    N: parseFloat(document.getElementById('crop-in-N')?.value || 90),
    P: parseFloat(document.getElementById('crop-in-P')?.value || 45),
    K: parseFloat(document.getElementById('crop-in-K')?.value || 40),
    temperature: parseFloat(document.getElementById('crop-in-temperature')?.value || 25.0),
    humidity: parseFloat(document.getElementById('crop-in-humidity')?.value || 80),
    ph: parseFloat(document.getElementById('crop-in-ph')?.value || 6.5),
    rainfall: parseFloat(document.getElementById('crop-in-rainfall')?.value || 220),
    model_name: document.getElementById('crop-model-select')?.value || "Random Forest"
  };

  try {
    const res = await fetch('/api/predict/crop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.success) {
      latestCropData = data;
      renderCropResult(data);
    }
  } catch (err) {
    console.error('Crop prediction fetch error:', err);
  } finally {
    if (!isSilent && submitBtn) {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  }
}

function renderCropResult(data) {
  const meta = data.metadata || {};
  const cropTitle = meta.title || data.crop.toUpperCase();
  const cropIcon = meta.icon || '🌱';
  const cropCategory = meta.category || 'Agricultural Crop';
  const cropDesc = meta.description || `Optimal match for ${data.crop}.`;
  const cropSeason = meta.growing_season || 'Standard Agronomic Cycle';
  const rationale = (data.scientific_rationale && data.scientific_rationale.length > 0)
    ? data.scientific_rationale.join(' ')
    : 'All soil and climatic parameters align with optimal crop physiology.';

  // 1. UPDATE IMMEDIATE INLINE RESULT CARD (Right beneath the button)
  const inlineBadge = document.getElementById('crop-inline-badge');
  if (inlineBadge) inlineBadge.innerText = `${data.model_used} • ${data.confidence.toFixed(1)}% Confidence`;

  const inlineIcon = document.getElementById('crop-inline-icon');
  if (inlineIcon) inlineIcon.innerText = cropIcon;

  const inlineName = document.getElementById('crop-inline-name');
  if (inlineName) inlineName.innerText = cropTitle;

  const inlineCat = document.getElementById('crop-inline-category');
  if (inlineCat) inlineCat.innerText = cropCategory;

  const inlineDesc = document.getElementById('crop-inline-desc');
  if (inlineDesc) inlineDesc.innerText = cropDesc;

  const inlineSeason = document.getElementById('crop-inline-season');
  if (inlineSeason) inlineSeason.innerText = cropSeason;

  const inlineRationale = document.getElementById('crop-inline-rationale');
  if (inlineRationale) inlineRationale.innerText = rationale;

  // Render Inline Probabilities List
  const inlineProbList = document.getElementById('crop-inline-probs');
  if (inlineProbList && data.probabilities) {
    const sorted = Object.entries(data.probabilities)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3);

    inlineProbList.innerHTML = sorted.map(([name, pct], idx) => `
      <div>
        <div class="flex justify-between text-[11px] mb-0.5">
          <span class="font-bold text-white capitalize flex items-center space-x-1.5">
            <span class="w-1.5 h-1.5 rounded-full ${idx === 0 ? 'bg-almond' : 'bg-matcha/40'}"></span>
            <span>${name}</span>
          </span>
          <span class="font-mono ${idx === 0 ? 'text-almond font-bold' : 'text-mint/70'}">${pct.toFixed(1)}%</span>
        </div>
        <div class="w-full bg-eclipse rounded-full h-1.5 overflow-hidden border border-roast-border">
          <div class="h-full rounded-full transition-all duration-300 ${idx === 0 ? 'bg-gradient-to-r from-almond to-matcha' : 'bg-almond/30'}" style="width: ${Math.max(pct, 2)}%"></div>
        </div>
      </div>
    `).join('');
  }

  // Visual pulse on inline card
  const inlineCard = document.getElementById('crop-inline-card');
  if (inlineCard) {
    inlineCard.classList.add('ring-4', 'ring-almond/50', 'scale-[1.01]');
    setTimeout(() => inlineCard.classList.remove('ring-4', 'ring-almond/50', 'scale-[1.01]'), 350);
  }

  // 2. UPDATE RIGHT-COLUMN RESULT CARD
  const iconDisp = document.getElementById('crop-icon-display');
  if (iconDisp) iconDisp.innerText = cropIcon;

  const catBadge = document.getElementById('crop-category-badge');
  if (catBadge) catBadge.innerText = cropCategory;

  const nameDisp = document.getElementById('crop-name-display');
  if (nameDisp) nameDisp.innerText = cropTitle;

  const descDisp = document.getElementById('crop-desc-display');
  if (descDisp) descDisp.innerText = cropDesc;

  const seasonDisp = document.getElementById('crop-season-display');
  if (seasonDisp) seasonDisp.innerText = cropSeason;

  const ratDisp = document.getElementById('crop-rationale-display');
  if (ratDisp) ratDisp.innerText = rationale;

  const badge = document.getElementById('crop-confidence-badge');
  if (badge) badge.innerText = `${data.model_used} • ${data.confidence.toFixed(1)}% Score`;

  // Cross-Model consensus
  const comp = data.multi_model_comparison;
  if (comp) {
    if (comp['Random Forest']) {
      const el = document.getElementById('crop-m1-pred');
      if (el) el.innerText = comp['Random Forest'].predicted_crop;
      const acc = document.getElementById('crop-m1-acc');
      if (acc) acc.innerText = `${comp['Random Forest'].confidence || '99.3'}% conf`;
    }
    if (comp['Decision Tree']) {
      const el = document.getElementById('crop-m2-pred');
      if (el) el.innerText = comp['Decision Tree'].predicted_crop;
      const acc = document.getElementById('crop-m2-acc');
      if (acc) acc.innerText = `${comp['Decision Tree'].confidence || '98.2'}% conf`;
    }
    if (comp['KNN']) {
      const el = document.getElementById('crop-m3-pred');
      if (el) el.innerText = comp['KNN'].predicted_crop;
      const acc = document.getElementById('crop-m3-acc');
      if (acc) acc.innerText = `${comp['KNN'].confidence || '97.5'}% conf`;
    }
  }

  // Right Column Probabilities Progress Bars
  const probList = document.getElementById('crop-probabilities-list');
  if (probList && data.probabilities) {
    const sorted = Object.entries(data.probabilities)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4);

    probList.innerHTML = sorted.map(([name, pct], idx) => `
      <div>
        <div class="flex justify-between text-xs mb-1">
          <span class="font-bold text-white capitalize flex items-center space-x-1.5">
            <span class="w-1.5 h-1.5 rounded-full ${idx === 0 ? 'bg-emerald-vibrant' : 'bg-mint/40'}"></span>
            <span>${name}</span>
          </span>
          <span class="font-mono ${idx === 0 ? 'text-emerald-vibrant font-bold' : 'text-mint/70'}">${pct.toFixed(1)}%</span>
        </div>
        <div class="w-full bg-pine/90 rounded-full h-2 overflow-hidden border border-emerald-vibrant/20">
          <div class="h-full rounded-full transition-all duration-300 ${idx === 0 ? 'bg-gradient-to-r from-emerald-vibrant to-apple' : 'bg-emerald-vibrant/40'}" style="width: ${Math.max(pct, 2)}%"></div>
        </div>
      </div>
    `).join('');
  }

  // Synchronize Farm Economics & Crop Rotation
  currentCropNameForEcon = data.crop;
  updateCropEconomics();
  updateCropRotation(data.crop);

  if (window.lucide) window.lucide.createIcons();
}

// ============================================================
// FERTILIZER PRESETS & INFERENCE
// ============================================================
const FERT_PRESETS = {
  sugarcane: { Soil_Type: 'Black', Crop_Type: 'Sugarcane', Moisture: 55, Temperature: 30, Humidity: 65, Nitrogen: 38, Phosphorous: 15, Potassium: 20 },
  paddy: { Soil_Type: 'Clayey', Crop_Type: 'Paddy', Moisture: 60, Temperature: 26, Humidity: 75, Nitrogen: 25, Phosphorous: 32, Potassium: 18 },
  wheat: { Soil_Type: 'Loamy', Crop_Type: 'Wheat', Moisture: 38, Temperature: 22, Humidity: 50, Nitrogen: 28, Phosphorous: 24, Potassium: 16 },
  cotton: { Soil_Type: 'Red', Crop_Type: 'Cotton', Moisture: 35, Temperature: 32, Humidity: 45, Nitrogen: 18, Phosphorous: 14, Potassium: 30 }
};

function loadFertPreset(name) {
  const p = FERT_PRESETS[name];
  if (!p) return;

  const soilEl = document.getElementById('fert-soil-type');
  if (soilEl) soilEl.value = p.Soil_Type;
  const cropEl = document.getElementById('fert-crop-type');
  if (cropEl) cropEl.value = p.Crop_Type;

  const setVal = (key, val) => {
    const s = document.getElementById(`fert-in-${key}`);
    const n = document.getElementById(`fert-num-${key}`);
    if (s) s.value = val;
    if (n) n.value = val;
  };

  setVal('Moisture', p.Moisture);
  setVal('Temperature', p.Temperature);
  setVal('Humidity', p.Humidity);
  setVal('Nitrogen', p.Nitrogen);
  setVal('Phosphorous', p.Phosphorous);
  setVal('Potassium', p.Potassium);

  executeFertPrediction(false);
}

async function handleFertPredict(e) {
  if (e) e.preventDefault();
  await executeFertPrediction(false);
}

async function executeFertPrediction(isSilent = false) {
  const submitBtn = document.getElementById('fert-submit-btn');
  const originalText = submitBtn ? submitBtn.innerHTML : '';

  if (!isSilent && submitBtn) {
    submitBtn.innerHTML = `<span class="inline-block animate-spin mr-2">⏳</span> Computing Prescription...`;
    submitBtn.disabled = true;
  }

  const payload = {
    Soil_Type: document.getElementById('fert-soil-type')?.value || 'Loamy',
    Crop_Type: document.getElementById('fert-crop-type')?.value || 'Sugarcane',
    Moisture: parseFloat(document.getElementById('fert-in-Moisture')?.value || 45),
    Temperature: parseFloat(document.getElementById('fert-in-Temperature')?.value || 28),
    Humidity: parseFloat(document.getElementById('fert-in-Humidity')?.value || 60),
    Nitrogen: parseFloat(document.getElementById('fert-in-Nitrogen')?.value || 22),
    Phosphorous: parseFloat(document.getElementById('fert-in-Phosphorous')?.value || 18),
    Potassium: parseFloat(document.getElementById('fert-in-Potassium')?.value || 14),
    model_name: document.getElementById('fert-model-select')?.value || "Random Forest"
  };

  try {
    const res = await fetch('/api/predict/fertilizer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.success) {
      latestFertData = data;
      renderFertResult(data);
    }
  } catch (err) {
    console.error('Fertilizer fetch error:', err);
  } finally {
    if (!isSilent && submitBtn) {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  }
}

function renderFertResult(data) {
  const meta = data.metadata || {};
  const fertName = data.fertilizer;
  const formulaText = `NPK: ${meta.npk || meta.formula || 'Commercial Formulation'}`;
  const fertDesc = meta.description || 'Targeted mineral fertilizer formulation.';
  const fertAdvice = meta.usage_advice || 'Incorporate evenly into topsoil and water thoroughly.';
  const diagText = (data.diagnostics && data.diagnostics.length > 0)
    ? data.diagnostics.join(' ')
    : 'Soil chemical profile is adequately buffered for crop uptake.';

  // 1. UPDATE IMMEDIATE INLINE RESULT CARD (Right beneath the button)
  const inlineBadge = document.getElementById('fert-inline-badge');
  if (inlineBadge) inlineBadge.innerText = `${data.model_used} • ${data.confidence.toFixed(1)}% Confidence`;

  const inlineName = document.getElementById('fert-inline-name');
  if (inlineName) inlineName.innerText = fertName;

  const inlineFormula = document.getElementById('fert-inline-formula');
  if (inlineFormula) inlineFormula.innerText = formulaText;

  const inlineDesc = document.getElementById('fert-inline-desc');
  if (inlineDesc) inlineDesc.innerText = fertDesc;

  const inlineAdvice = document.getElementById('fert-inline-advice');
  if (inlineAdvice) inlineAdvice.innerText = fertAdvice;

  const inlineDiag = document.getElementById('fert-inline-diagnostic');
  if (inlineDiag) inlineDiag.innerText = diagText;

  // Render Inline Probabilities List
  const inlineProbList = document.getElementById('fert-inline-probs');
  if (inlineProbList && data.probabilities) {
    const sorted = Object.entries(data.probabilities)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3);

    inlineProbList.innerHTML = sorted.map(([name, pct], idx) => `
      <div>
        <div class="flex justify-between text-[11px] mb-0.5">
          <span class="font-bold text-white font-mono flex items-center space-x-1.5">
            <span class="w-1.5 h-1.5 rounded-full ${idx === 0 ? 'bg-matcha' : 'bg-almond/30'}"></span>
            <span>${name}</span>
          </span>
          <span class="font-mono ${idx === 0 ? 'text-matcha font-bold' : 'text-mint/70'}">${pct.toFixed(1)}%</span>
        </div>
        <div class="w-full bg-eclipse rounded-full h-1.5 overflow-hidden border border-roast-border">
          <div class="h-full rounded-full transition-all duration-300 ${idx === 0 ? 'bg-gradient-to-r from-matcha to-almond' : 'bg-matcha/30'}" style="width: ${Math.max(pct, 2)}%"></div>
        </div>
      </div>
    `).join('');
  }

  // Visual pulse on inline card
  const inlineCard = document.getElementById('fert-inline-card');
  if (inlineCard) {
    inlineCard.classList.add('ring-4', 'ring-matcha/50', 'scale-[1.01]');
    setTimeout(() => inlineCard.classList.remove('ring-4', 'ring-matcha/50', 'scale-[1.01]'), 350);
  }

  // 2. UPDATE RIGHT-COLUMN RESULT CARD
  const formulaBadge = document.getElementById('fert-formula-badge');
  if (formulaBadge) formulaBadge.innerText = formulaText;

  const nameDisp = document.getElementById('fert-name-display');
  if (nameDisp) nameDisp.innerText = fertName;

  const descDisp = document.getElementById('fert-desc-display');
  if (descDisp) descDisp.innerText = fertDesc;

  const adviceDisp = document.getElementById('fert-advice-display');
  if (adviceDisp) adviceDisp.innerText = fertAdvice;

  const diagDisp = document.getElementById('fert-diagnostic-display');
  if (diagDisp) diagDisp.innerText = diagText;

  const badge = document.getElementById('fert-confidence-badge');
  if (badge) badge.innerText = `${data.model_used} • ${data.confidence.toFixed(1)}% Score`;

  // Cross-Model consensus
  const comp = data.multi_model_comparison;
  if (comp) {
    if (comp['Random Forest']) {
      const el = document.getElementById('fert-m1-pred');
      if (el) el.innerText = comp['Random Forest'].predicted_fertilizer;
      const acc = document.getElementById('fert-m1-acc');
      if (acc) acc.innerText = `${comp['Random Forest'].confidence || '98.0'}% conf`;
    }
    if (comp['Decision Tree']) {
      const el = document.getElementById('fert-m2-pred');
      if (el) el.innerText = comp['Decision Tree'].predicted_fertilizer;
      const acc = document.getElementById('fert-m2-acc');
      if (acc) acc.innerText = `${comp['Decision Tree'].confidence || '95.0'}% conf`;
    }
    if (comp['KNN']) {
      const el = document.getElementById('fert-m3-pred');
      if (el) el.innerText = comp['KNN'].predicted_fertilizer;
      const acc = document.getElementById('fert-m3-acc');
      if (acc) acc.innerText = `${comp['KNN'].confidence || '88.5'}% conf`;
    }
  }

  // Right Column Probabilities Progress Bars
  const probList = document.getElementById('fert-probabilities-list');
  if (probList && data.probabilities) {
    const sorted = Object.entries(data.probabilities)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4);

    probList.innerHTML = sorted.map(([name, pct], idx) => `
      <div>
        <div class="flex justify-between text-xs mb-1">
          <span class="font-bold text-white font-mono flex items-center space-x-1.5">
            <span class="w-1.5 h-1.5 rounded-full ${idx === 0 ? 'bg-apple' : 'bg-mint/40'}"></span>
            <span>${name}</span>
          </span>
          <span class="font-mono ${idx === 0 ? 'text-apple font-bold' : 'text-mint/70'}">${pct.toFixed(1)}%</span>
        </div>
        <div class="w-full bg-pine/90 rounded-full h-2 overflow-hidden border border-emerald-vibrant/20">
          <div class="h-full rounded-full transition-all duration-300 ${idx === 0 ? 'bg-gradient-to-r from-apple to-emerald-vibrant' : 'bg-apple/40'}" style="width: ${Math.max(pct, 2)}%"></div>
        </div>
      </div>
    `).join('');
  }

  // Synchronize Commercial Bag-Level Fertilizer Dosage
  currentFertNameForDosage = data.fertilizer;
  updateFertilizerDosage();

  if (window.lucide) window.lucide.createIcons();
}

// ============================================================
// SOIL HEALTH CARD LIVE SYNCHRONIZATION
// ============================================================
function syncSoilReport() {
  const dateEl = document.getElementById('shc-report-date');
  if (dateEl) {
    const today = new Date();
    dateEl.innerText = today.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  }

  // Read active inputs
  const N = parseFloat(document.getElementById('crop-in-N')?.value || document.getElementById('fert-in-Nitrogen')?.value || 90);
  const P = parseFloat(document.getElementById('crop-in-P')?.value || document.getElementById('fert-in-Phosphorous')?.value || 45);
  const K = parseFloat(document.getElementById('crop-in-K')?.value || document.getElementById('fert-in-Potassium')?.value || 40);
  const pH = parseFloat(document.getElementById('crop-in-ph')?.value || 6.5);
  const moisture = parseFloat(document.getElementById('fert-in-Moisture')?.value || 45);
  const soilType = document.getElementById('fert-soil-type')?.value || 'Loamy';
  const cropContext = document.getElementById('fert-crop-type')?.value || 'Sugarcane';

  // Profile
  const soilTypeEl = document.getElementById('shc-soil-type');
  if (soilTypeEl) soilTypeEl.innerText = `${soilType} Soil`;

  const cropContextEl = document.getElementById('shc-crop-context');
  if (cropContextEl) cropContextEl.innerText = cropContext;

  // Nitrogen Audit
  const valN = document.getElementById('shc-val-N');
  const statusN = document.getElementById('shc-status-N');
  const actionN = document.getElementById('shc-action-N');
  if (valN) valN.innerText = `${N.toFixed(0)} kg/ha`;
  if (statusN) {
    if (N < 40) {
      statusN.innerHTML = `<span class="px-2 py-0.5 rounded bg-rose-900/60 text-rose-300 border border-rose-500/40 font-bold">DEFICIENT</span>`;
      if (actionN) actionN.innerText = 'Immediate top-dressing with Urea (46-0-0) required at 50 kg/ha.';
    } else if (N > 110) {
      statusN.innerHTML = `<span class="px-2 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-500/40 font-bold">EXCESS</span>`;
      if (actionN) actionN.innerText = 'Halt synthetic nitrogen to avoid vegetative overgrowth and lodging.';
    } else {
      statusN.innerHTML = `<span class="px-2 py-0.5 rounded bg-pine text-emerald-vibrant border border-emerald-vibrant/40 font-bold">OPTIMAL</span>`;
      if (actionN) actionN.innerText = 'Adequate vegetative nitrogen reserves. Maintain maintenance dressing.';
    }
  }

  // Phosphorus Audit
  const valP = document.getElementById('shc-val-P');
  const statusP = document.getElementById('shc-status-P');
  const actionP = document.getElementById('shc-action-P');
  if (valP) valP.innerText = `${P.toFixed(0)} kg/ha`;
  if (statusP) {
    if (P < 25) {
      statusP.innerHTML = `<span class="px-2 py-0.5 rounded bg-rose-900/60 text-rose-300 border border-rose-500/40 font-bold">DEFICIENT</span>`;
      if (actionP) actionP.innerText = 'Apply DAP (18-46-0) basal furrow dressing during sowing.';
    } else {
      statusP.innerHTML = `<span class="px-2 py-0.5 rounded bg-pine text-apple border border-apple/40 font-bold">NORMAL</span>`;
      if (actionP) actionP.innerText = 'Sufficient for seedling root proliferation and energetic ATP synthesis.';
    }
  }

  // Potassium Audit
  const valK = document.getElementById('shc-val-K');
  const statusK = document.getElementById('shc-status-K');
  const actionK = document.getElementById('shc-action-K');
  if (valK) valK.innerText = `${K.toFixed(0)} kg/ha`;
  if (statusK) {
    if (K < 25) {
      statusK.innerHTML = `<span class="px-2 py-0.5 rounded bg-rose-900/60 text-rose-300 border border-rose-500/40 font-bold">DEFICIENT</span>`;
      if (actionK) actionK.innerText = 'Apply Muriate of Potash (MOP / 0-0-60) to avoid drought and lodging risks.';
    } else {
      statusK.innerHTML = `<span class="px-2 py-0.5 rounded bg-pine text-mint border border-mint/40 font-bold">NORMAL</span>`;
      if (actionK) actionK.innerText = 'Supports cellular turgor, stomatal regulation, and disease resistance.';
    }
  }

  // pH Audit
  const valPh = document.getElementById('shc-val-ph');
  const statusPh = document.getElementById('shc-status-ph');
  const actionPh = document.getElementById('shc-action-ph');
  if (valPh) valPh.innerText = `${pH.toFixed(2)} pH`;
  if (statusPh) {
    if (pH < 6.0) {
      statusPh.innerHTML = `<span class="px-2 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-500/40 font-bold">ACIDIC</span>`;
      if (actionPh) actionPh.innerText = 'Apply agricultural lime (CaCO3) at 400 kg/ha to neutralize soil acidity.';
    } else if (pH > 7.8) {
      statusPh.innerHTML = `<span class="px-2 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-500/40 font-bold">ALKALINE</span>`;
      if (actionPh) actionPh.innerText = 'Apply gypsum (CaSO4·2H2O) at 350 kg/ha to alleviate alkali sodium buildup.';
    } else {
      statusPh.innerHTML = `<span class="px-2 py-0.5 rounded bg-pine text-emerald-vibrant border border-emerald-vibrant/40 font-bold">NEUTRAL</span>`;
      if (actionPh) actionPh.innerText = 'Ideal chemical window for maximum micro and macro-nutrient bio-availability.';
    }
  }

  // Moisture Audit
  const valMoist = document.getElementById('shc-val-moisture');
  const statusMoist = document.getElementById('shc-status-moisture');
  const actionMoist = document.getElementById('shc-action-moisture');
  if (valMoist) valMoist.innerText = `${moisture.toFixed(1)}%`;
  if (statusMoist) {
    if (moisture < 30) {
      statusMoist.innerHTML = `<span class="px-2 py-0.5 rounded bg-amber-900/60 text-amber-300 border border-amber-500/40 font-bold">LOW</span>`;
      if (actionMoist) actionMoist.innerText = 'Irrigate before chemical fertilizer application to prevent osmotic root scorch.';
    } else {
      statusMoist.innerHTML = `<span class="px-2 py-0.5 rounded bg-pine text-mint border border-mint/40 font-bold">SUFFICIENT</span>`;
      if (actionMoist) actionMoist.innerText = 'Soil field capacity is primed for immediate basal nutrient uptake.';
    }
  }

  // Populate latest prediction outputs
  if (latestCropData) {
    const meta = latestCropData.metadata || {};
    const iconEl = document.getElementById('shc-crop-icon');
    if (iconEl) iconEl.innerText = meta.icon || '🌱';
    const nameEl = document.getElementById('shc-crop-name');
    if (nameEl) nameEl.innerText = meta.title || latestCropData.crop.toUpperCase();
    const seasonEl = document.getElementById('shc-crop-season');
    if (seasonEl) seasonEl.innerText = meta.growing_season || 'Standard Growing Cycle';
    const confEl = document.getElementById('shc-crop-conf');
    if (confEl) confEl.innerText = `${latestCropData.confidence.toFixed(1)}% Conf`;
    const advEl = document.getElementById('shc-crop-advice');
    if (advEl) advEl.innerText = meta.description || 'Target agronomic recommendation based on active parameters.';
  }

  if (latestFertData) {
    const meta = latestFertData.metadata || {};
    const nameEl = document.getElementById('shc-fert-name');
    if (nameEl) nameEl.innerText = latestFertData.fertilizer;
    const formEl = document.getElementById('shc-fert-formula');
    if (formEl) formEl.innerText = `NPK Ratio: ${meta.npk || meta.formula || 'Compound'}`;
    const confEl = document.getElementById('shc-fert-conf');
    if (confEl) confEl.innerText = `${latestFertData.confidence.toFixed(1)}% Conf`;
    const advEl = document.getElementById('shc-fert-advice');
    if (advEl) advEl.innerText = meta.usage_advice || 'Incorporate evenly into topsoil before irrigation.';
  }

  if (window.lucide) window.lucide.createIcons();
}

// ============================================================
// INTERACTIVE DATASET EXPLORER
// ============================================================
let currentDatasetType = 'crop';
let currentDatasetData = [];
let currentDatasetColumns = [];

function switchDatasetView(type) {
  currentDatasetType = type;
  const btnCrop = document.getElementById('dset-btn-crop');
  const btnFert = document.getElementById('dset-btn-fert');

  if (type === 'crop') {
    if (btnCrop) {
      btnCrop.className = 'px-3.5 py-2 text-xs font-bold rounded-lg bg-almond text-eclipse transition-all shadow-almond-glow flex items-center space-x-1.5';
    }
    if (btnFert) {
      btnFert.className = 'px-3.5 py-2 text-xs font-semibold rounded-lg text-almond/80 hover:text-white transition-all flex items-center space-x-1.5';
    }
  } else {
    if (btnFert) {
      btnFert.className = 'px-3.5 py-2 text-xs font-bold rounded-lg bg-matcha text-white transition-all shadow-matcha-glow flex items-center space-x-1.5';
    }
    if (btnCrop) {
      btnCrop.className = 'px-3.5 py-2 text-xs font-semibold rounded-lg text-almond/80 hover:text-white transition-all flex items-center space-x-1.5';
    }
  }

  loadDatasetExplorer(type);
}

async function loadDatasetExplorer(type) {
  const container = document.getElementById('dataset-table-view-container');
  if (!container) return;

  container.innerHTML = `<p class="text-mint py-12 text-center flex items-center justify-center gap-2"><span class="animate-spin text-lg">⏳</span> Loading ${type === 'crop' ? 'Crop Recommendation' : 'Fertilizer Prediction'} dataset records...</p>`;

  const endpoint = type === 'crop' ? '/api/data/crop/sample?limit=50' : '/api/data/fertilizer/sample?limit=50';

  try {
    const res = await fetch(endpoint);
    const result = await res.json();

    currentDatasetData = result.data || [];
    currentDatasetColumns = result.columns || [];

    // Update stat cards
    const recsEl = document.getElementById('dset-stat-records');
    if (recsEl) recsEl.innerText = (result.total_rows || 200).toLocaleString();

    const featsEl = document.getElementById('dset-stat-features');
    if (featsEl) featsEl.innerText = currentDatasetColumns.length.toString();

    const classEl = document.getElementById('dset-stat-classes');
    if (classEl) classEl.innerText = type === 'crop' ? '22 Target Crops' : '7 Formulations';

    const metricEl = document.getElementById('dset-stat-metric');
    if (metricEl && result.summary) {
      if (type === 'crop' && result.summary.N) {
        metricEl.innerText = `${result.summary.N.mean} kg/ha`;
      } else if (type === 'fertilizer' && result.summary.Moisture) {
        metricEl.innerText = `${result.summary.Moisture.mean}%`;
      }
    }

    renderDatasetRows(currentDatasetData);
  } catch (err) {
    container.innerHTML = `<p class="text-rose-400 py-8 text-center">Failed to load dataset: ${err.message}</p>`;
  }
}

function renderDatasetRows(rows) {
  const container = document.getElementById('dataset-table-view-container');
  const indicator = document.getElementById('dset-rows-indicator');
  if (!container) return;

  if (indicator) {
    indicator.innerText = `Showing ${rows.length} records`;
  }

  if (rows.length === 0) {
    container.innerHTML = `<p class="text-mint/60 py-12 text-center">No matching dataset records found for your search query.</p>`;
    return;
  }

  let html = `<table class="w-full text-left divide-y divide-pine-border">
    <thead class="bg-pine text-mint uppercase font-mono text-[10px] sticky top-0 z-10">
      <tr>
        <th class="py-3 px-3.5 text-center text-mint/60">#</th>
        ${currentDatasetColumns.map(col => `<th class="py-3 px-3.5 whitespace-nowrap">${col}</th>`).join('')}
      </tr>
    </thead>
    <tbody class="divide-y divide-pine-border text-slate-200 text-xs">
      ${rows.map((row, idx) => `
        <tr class="hover:bg-pine/30 transition-colors">
          <td class="py-2.5 px-3.5 text-center font-mono text-mint/50">${idx + 1}</td>
          ${currentDatasetColumns.map(col => {
            const val = row[col];
            if (col === 'label') {
              return `<td class="py-2.5 px-3.5 whitespace-nowrap"><span class="px-2.5 py-0.5 rounded-full bg-pine text-emerald-vibrant border border-emerald-vibrant/40 font-bold capitalize">${val}</span></td>`;
            }
            if (col === 'Fertilizer Name') {
              return `<td class="py-2.5 px-3.5 whitespace-nowrap"><span class="px-2.5 py-0.5 rounded-full bg-pine text-apple border border-apple/40 font-bold">${val}</span></td>`;
            }
            if (col === 'Soil Type' || col === 'Crop Type') {
              return `<td class="py-2.5 px-3.5 whitespace-nowrap font-bold text-mint">${val}</td>`;
            }
            const num = typeof val === 'number' ? (val % 1 !== 0 ? val.toFixed(1) : val) : val;
            return `<td class="py-2.5 px-3.5 whitespace-nowrap font-mono text-slate-300">${num}</td>`;
          }).join('')}
        </tr>
      `).join('')}
    </tbody>
  </table>`;

  container.innerHTML = html;
}

function filterDatasetRows(query) {
  if (!currentDatasetData || currentDatasetData.length === 0) return;
  const q = (query || '').toLowerCase().trim();
  if (!q) {
    renderDatasetRows(currentDatasetData);
    return;
  }

  const filtered = currentDatasetData.filter(row => {
    return Object.values(row).some(v => String(v).toLowerCase().includes(q));
  });

  renderDatasetRows(filtered);
}

function reloadDatasetView() {
  const searchInput = document.getElementById('dataset-search-input');
  if (searchInput) searchInput.value = '';
  loadDatasetExplorer(currentDatasetType);
}

// ============================================================
// EDA GALLERY FILTER & LIGHTBOX
// ============================================================
function filterGallery(type) {
  const cropItems = document.querySelectorAll('.gallery-crop');
  const fertItems = document.querySelectorAll('.gallery-fert');
  const btnCrop = document.getElementById('gallery-filter-crop');
  const btnFert = document.getElementById('gallery-filter-fert');

  if (type === 'crop') {
    cropItems.forEach(el => el.classList.remove('hidden'));
    fertItems.forEach(el => el.classList.add('hidden'));

    if (btnCrop) {
      btnCrop.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-almond text-eclipse transition-colors shadow-almond-glow';
    }
    if (btnFert) {
      btnFert.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-roast hover:bg-roast-elevated text-almond/80 transition-colors border border-almond/20';
    }
  } else {
    cropItems.forEach(el => el.classList.add('hidden'));
    fertItems.forEach(el => el.classList.remove('hidden'));

    if (btnFert) {
      btnFert.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-almond text-eclipse transition-colors shadow-almond-glow';
    }
    if (btnCrop) {
      btnCrop.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-roast hover:bg-roast-elevated text-almond/80 transition-colors border border-almond/20';
    }
  }
}

function openLightbox(imgSrc, title) {
  const modal = document.getElementById('lightbox-modal');
  const img = document.getElementById('lightbox-img');
  const titleEl = document.getElementById('lightbox-title');

  if (modal && img) {
    img.src = imgSrc;
    if (titleEl) titleEl.innerText = title;
    modal.classList.remove('hidden');
  }
}

function closeLightbox() {
  const modal = document.getElementById('lightbox-modal');
  if (modal) modal.classList.add('hidden');
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeLightbox();
  }
});

// ============================================================
// FARMER DECISION SUITE: ECONOMICS, CLIMATE STRESS & ROTATION
// ============================================================
let currentCropNameForEcon = 'rice';

function setLandArea(acres) {
  const input = document.getElementById('econ-acres-input');
  if (input) input.value = acres;
  updateCropEconomics();
}

async function updateCropEconomics() {
  const acresInput = document.getElementById('econ-acres-input');
  const acres = parseFloat(acresInput ? acresInput.value : 2.5) || 2.5;
  const crop = currentCropNameForEcon || 'rice';

  try {
    const res = await fetch('/api/farmer/profitability', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ crop_name: crop, land_area_acres: acres })
    });
    const data = await res.json();
    if (data.success) {
      const yieldEl = document.getElementById('econ-yield-val');
      if (yieldEl) yieldEl.innerText = data.expected_yield_quintals.toLocaleString();

      const yieldSub = document.getElementById('econ-yield-sub');
      if (yieldSub) yieldSub.innerText = `@ ${data.yield_per_acre} Q / Acre`;

      const revEl = document.getElementById('econ-revenue-val');
      if (revEl) revEl.innerText = Math.round(data.gross_revenue_inr).toLocaleString();

      const revSub = document.getElementById('econ-revenue-sub');
      if (revSub) revSub.innerText = `MSP: ₹${data.msp_per_quintal.toLocaleString()} / Q`;

      const costEl = document.getElementById('econ-cost-val');
      if (costEl) costEl.innerText = Math.round(data.production_cost_inr).toLocaleString();

      const profitEl = document.getElementById('econ-profit-val');
      if (profitEl) profitEl.innerText = Math.round(data.net_profit_inr).toLocaleString();

      const roiBadge = document.getElementById('econ-roi-badge');
      if (roiBadge) roiBadge.innerText = `+${data.roi_percentage}% ROI`;

      const marketSub = document.getElementById('econ-market-sub');
      if (marketSub) marketSub.innerText = `Market Demand: ${data.market_demand} • Risk: ${data.risk_level}`;
    }
  } catch (err) {
    console.error('Profitability fetch error:', err);
  }
}

// Climate Stress Simulation
let stressCache = null;

async function simulateClimateStress(scenarioId) {
  const payload = {
    N: parseFloat(document.getElementById('crop-in-N')?.value || 90),
    P: parseFloat(document.getElementById('crop-in-P')?.value || 45),
    K: parseFloat(document.getElementById('crop-in-K')?.value || 40),
    temperature: parseFloat(document.getElementById('crop-in-temperature')?.value || 25.0),
    humidity: parseFloat(document.getElementById('crop-in-humidity')?.value || 80),
    ph: parseFloat(document.getElementById('crop-in-ph')?.value || 6.5),
    rainfall: parseFloat(document.getElementById('crop-in-rainfall')?.value || 220),
    model_name: "Random Forest"
  };

  try {
    const res = await fetch('/api/farmer/climate-stress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success && data.scenarios) {
      stressCache = data.scenarios;
      const match = data.scenarios.find(s => s.scenario_id === scenarioId);
      if (match) {
        // Highlight active button
        ['drought', 'heatwave', 'excess_rain'].forEach(id => {
          const btn = document.getElementById(`stress-btn-${id}`);
          if (btn) {
            if (id === scenarioId) {
              btn.classList.add('ring-2', 'ring-almond', 'bg-roast');
            } else {
              btn.classList.remove('ring-2', 'ring-almond', 'bg-roast');
            }
          }
        });

        const titleEl = document.getElementById('stress-active-title');
        if (titleEl) titleEl.innerHTML = `<span>${match.icon}</span> <span>${match.scenario_name} Active</span>`;

        const badgeEl = document.getElementById('stress-crop-badge');
        if (badgeEl) badgeEl.innerText = `${match.confidence}% Confidence`;

        const iconEl = document.getElementById('stress-crop-icon');
        if (iconEl) iconEl.innerText = match.crop_meta.icon || '🌱';

        const nameEl = document.getElementById('stress-crop-name');
        if (nameEl) nameEl.innerText = `${match.crop_meta.title || match.predicted_resilient_crop} (Resilient Match)`;

        const descEl = document.getElementById('stress-desc');
        if (descEl) {
          descEl.innerText = `${match.description} Perturbed conditions: Temp ${match.simulated_params.temperature}°C, Humidity ${match.simulated_params.humidity}%, Rain ${match.simulated_params.rainfall}mm. Machine Learning algorithm identifies ${match.predicted_resilient_crop} as the maximum-yield climate-resilient alternative.`;
        }
      }
    }
  } catch (err) {
    console.error('Climate stress simulation error:', err);
  }
}

function resetClimateStress() {
  ['drought', 'heatwave', 'excess_rain'].forEach(id => {
    const btn = document.getElementById(`stress-btn-${id}`);
    if (btn) btn.classList.remove('ring-2', 'ring-almond', 'bg-roast');
  });

  const titleEl = document.getElementById('stress-active-title');
  if (titleEl) titleEl.innerHTML = `<i data-lucide="info" class="w-3.5 h-3.5 text-almond"></i> <span>Baseline Conditions Active</span>`;

  const badgeEl = document.getElementById('stress-crop-badge');
  if (badgeEl) badgeEl.innerText = `Live Model Evaluated`;

  const iconEl = document.getElementById('stress-crop-icon');
  if (iconEl && latestCropData) iconEl.innerText = latestCropData.metadata?.icon || '🌾';

  const nameEl = document.getElementById('stress-crop-name');
  if (nameEl && latestCropData) nameEl.innerText = `${latestCropData.crop.toUpperCase()} (Baseline Recommendation)`;

  const descEl = document.getElementById('stress-desc');
  if (descEl) descEl.innerText = 'Click any extreme weather shock toggle above to stress-test your farm parameters against Random Forest tree splits.';

  if (window.lucide) window.lucide.createIcons();
}

// Crop Rotation
async function updateCropRotation(cropName) {
  const crop = cropName || currentCropNameForEcon || 'rice';
  try {
    const res = await fetch(`/api/farmer/crop-rotation?crop_name=${encodeURIComponent(crop)}`);
    const data = await res.json();
    if (data.success && data.rotation_plan) {
      const plan = data.rotation_plan;
      const labelEl = document.getElementById('rotation-crop-label');
      if (labelEl) labelEl.innerText = `${crop.toUpperCase()} Cycle`;

      const s1Title = document.getElementById('rot-s1-title');
      if (s1Title) s1Title.innerText = plan.season_1.name;
      const s1Season = document.getElementById('rot-s1-season');
      if (s1Season) s1Season.innerText = plan.season_1.season;
      const s1Role = document.getElementById('rot-s1-role');
      if (s1Role) s1Role.innerText = plan.season_1.role;

      const s2Title = document.getElementById('rot-s2-title');
      if (s2Title) s2Title.innerText = plan.season_2.name;
      const s2Season = document.getElementById('rot-s2-season');
      if (s2Season) s2Season.innerText = plan.season_2.season;
      const s2Role = document.getElementById('rot-s2-role');
      if (s2Role) s2Role.innerText = plan.season_2.role;

      const s3Title = document.getElementById('rot-s3-title');
      if (s3Title) s3Title.innerText = plan.season_3.name;
      const s3Season = document.getElementById('rot-s3-season');
      if (s3Season) s3Season.innerText = plan.season_3.season;
      const s3Role = document.getElementById('rot-s3-role');
      if (s3Role) s3Role.innerText = plan.season_3.role;

      const benefitsEl = document.getElementById('rotation-benefits');
      if (benefitsEl && plan.benefits) {
        benefitsEl.innerHTML = `
          <div class="flex items-center space-x-1.5 font-bold text-almond mb-1">
            <i data-lucide="shield-check" class="w-3.5 h-3.5 text-almond"></i>
            <span>Ecological &amp; Soil Benefits:</span>
          </div>
          ${plan.benefits.map(b => `<p>• ${b}</p>`).join('')}
        `;
        if (window.lucide) window.lucide.createIcons();
      }
    }
  } catch (err) {
    console.error('Crop rotation error:', err);
  }
}

// ============================================================
// COMMERCIAL BAG-LEVEL FERTILIZER DOSAGE & SAVINGS AUDITOR
// ============================================================
let currentFertNameForDosage = '14-35-14';

function setFertLandArea(acres) {
  const input = document.getElementById('fert-acres-input');
  if (input) input.value = acres;
  updateFertilizerDosage();
}

async function updateFertilizerDosage() {
  const acresInput = document.getElementById('fert-acres-input');
  const acres = parseFloat(acresInput ? acresInput.value : 2.5) || 2.5;
  const fert = currentFertNameForDosage || '14-35-14';

  try {
    const res = await fetch('/api/farmer/fertilizer-dosage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fertilizer_name: fert, land_area_acres: acres })
    });
    const data = await res.json();
    if (data.success) {
      const bagsEl = document.getElementById('fert-bags-val');
      if (bagsEl) bagsEl.innerText = data.recommended_bags_50kg.toFixed(1);

      const weightEl = document.getElementById('fert-weight-val');
      if (weightEl) weightEl.innerText = `Total Weight: ${data.total_weight_kg.toLocaleString()} kg`;

      const costEl = document.getElementById('fert-cost-val');
      if (costEl) costEl.innerText = Math.round(data.estimated_cost_inr).toLocaleString();

      const overuseEl = document.getElementById('fert-overuse-val');
      if (overuseEl) overuseEl.innerText = data.conventional_overuse_bags.toFixed(1);

      const savingsEl = document.getElementById('fert-savings-val');
      if (savingsEl) savingsEl.innerText = Math.round(data.estimated_savings_inr).toLocaleString();

      const scheduleEl = document.getElementById('fert-schedule-text');
      if (scheduleEl) scheduleEl.innerText = data.application_schedule;

      const riskEl = document.getElementById('fert-risk-text');
      if (riskEl) riskEl.innerText = `${data.excess_toxicity_risk} Applying at the precision rate ensures target nutrient bioavailability with minimal chemical leaching.`;
    }
  } catch (err) {
    console.error('Fertilizer dosage error:', err);
  }
}

// ============================================================
// SATELLITE & AGRO-CLIMATE INTELLIGENCE (LEAFLET)
// ============================================================
let geoMap = null;
let currentGeoKey = 'chennai';
let currentGeoTelemetry = null;
let satLayer = null;
let streetLayer = null;
let activeMapLayerType = 'sat';
let geoMarker = null;
let geoCircle = null;

function initSatelliteMap() {
  const mapContainer = document.getElementById('geo-map');
  if (!mapContainer) return;

  if (geoMap) {
    geoMap.invalidateSize();
    return;
  }

  // Chennai Coordinates: [13.0827, 80.2707]
  geoMap = L.map('geo-map', {
    center: [13.0827, 80.2707],
    zoom: 11,
    zoomControl: true
  });

  // Esri World Imagery (High-Resolution Satellite Earth Observation)
  satLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Earth Observation Imagery',
    maxZoom: 18
  });

  // OpenStreetMap Street View
  streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 18
  });

  // Default to Satellite Imagery
  satLayer.addTo(geoMap);

  // Custom Gold Pulse Marker
  const customIcon = L.divIcon({
    className: 'custom-geo-pin',
    html: `<div style="
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #D6BD98;
      border: 3px solid #1A3636;
      box-shadow: 0 0 15px rgba(214, 189, 152, 0.9);
      display: flex;
      align-items: center;
      justify-content: center;
    "><div style="width: 6px; height: 6px; border-radius: 50%; background: #1A3636;"></div></div>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });

  geoMarker = L.marker([13.0827, 80.2707], { icon: customIcon }).addTo(geoMap);
  geoMarker.bindPopup(`
    <div style="font-family: 'Outfit', sans-serif; color: #1A3636; padding: 4px;">
      <b style="font-size: 14px;">Chennai Agricultural Zone</b><br>
      <span style="font-size: 11px; color: #40534C;">Tamil Nadu • 13.0827° N, 80.2707° E</span><br>
      <span style="font-size: 11px; font-weight: bold; color: #677D6A;">NDVI Score: 0.68 (High Canopy)</span>
    </div>
  `);

  // Agro-Climatic Buffer Zone Circle (12km radius)
  geoCircle = L.circle([13.0827, 80.2707], {
    radius: 12000,
    color: '#D6BD98',
    fillColor: '#677D6A',
    fillOpacity: 0.18,
    weight: 1.5,
    dashArray: '4, 6'
  }).addTo(geoMap);

  // Load telemetry data for default Chennai
  selectGeoLocation('chennai');
}

let currentMapBand = 'sat';
function setMapBand(band) {
  currentMapBand = band;
  ['sat', 'ndvi', 'ndwi'].forEach(b => {
    const btn = document.getElementById(`band-btn-${b}`);
    if (btn) {
      if (b === band) {
        btn.className = 'px-2.5 py-1 text-xs font-bold rounded-lg bg-almond text-eclipse border border-almond transition-all shadow-sm';
      } else {
        btn.className = 'px-2.5 py-1 text-xs font-semibold rounded-lg bg-roast hover:bg-roast-elevated text-mint border border-roast-border hover:border-matcha transition-all';
      }
    }
  });

  if (!geoCircle || !geoMap) return;

  if (band === 'sat') {
    geoCircle.setStyle({
      color: '#D6BD98',
      fillColor: '#677D6A',
      fillOpacity: 0.18,
      weight: 1.5,
      dashArray: '4, 6'
    });
  } else if (band === 'ndvi') {
    geoCircle.setStyle({
      color: '#4ade80',
      fillColor: '#22c55e',
      fillOpacity: 0.40,
      weight: 2.5,
      dashArray: null
    });
  } else if (band === 'ndwi') {
    geoCircle.setStyle({
      color: '#22d3ee',
      fillColor: '#06b6d4',
      fillOpacity: 0.38,
      weight: 2.5,
      dashArray: null
    });
  }
}

function toggleMapLayer() {
  if (!geoMap || !satLayer || !streetLayer) return;
  const btn = document.getElementById('map-layer-btn');
  if (activeMapLayerType === 'sat') {
    geoMap.removeLayer(satLayer);
    streetLayer.addTo(geoMap);
    activeMapLayerType = 'street';
    if (btn) btn.innerText = 'Toggle Satellite';
  } else {
    geoMap.removeLayer(streetLayer);
    satLayer.addTo(geoMap);
    activeMapLayerType = 'sat';
    if (btn) btn.innerText = 'Toggle Streets';
  }
}

async function selectGeoLocation(locKey) {
  currentGeoKey = locKey;

  // Update chip styles
  ['chennai', 'thanjavur', 'coimbatore', 'ludhiana', 'nashik'].forEach(k => {
    const chip = document.getElementById(`geo-chip-${k}`);
    if (chip) {
      if (k === locKey) {
        chip.className = 'geo-chip px-3 py-1.5 text-xs font-bold rounded-lg bg-almond text-eclipse border border-almond transition-all shadow-almond-glow';
      } else {
        chip.className = 'geo-chip px-3 py-1.5 text-xs font-semibold rounded-lg bg-roast hover:bg-roast-elevated text-mint hover:text-white border border-roast-border transition-all';
      }
    }
  });

  try {
    const res = await fetch(`/api/geo/analyze?location=${locKey}`);
    const data = await res.json();
    if (data.success) {
      currentGeoTelemetry = data;

      // Update Map View
      if (geoMap) {
        geoMap.flyTo([data.lat, data.lng], 11, { duration: 1.2 });
        if (geoMarker) {
          geoMarker.setLatLng([data.lat, data.lng]);
          geoMarker.setPopupContent(`
            <div style="font-family: 'Outfit', sans-serif; color: #1A3636; padding: 4px;">
              <b style="font-size: 14px;">${data.name}</b><br>
              <span style="font-size: 11px; color: #40534C;">${data.state} • ${data.lat.toFixed(4)}° N, ${data.lng.toFixed(4)}° E</span><br>
              <span style="font-size: 11px; font-weight: bold; color: #677D6A;">NDVI: ${data.ndvi_score} (${data.vegetation_status})</span>
            </div>
          `);
        }
        if (geoCircle) {
          geoCircle.setLatLng([data.lat, data.lng]);
        }
        setTimeout(() => geoMap.invalidateSize(), 200);
      }

      // Reset Map Band to sat
      setMapBand('sat');

      // Update UI Text Elements
      const titleEl = document.getElementById('geo-map-title');
      if (titleEl) titleEl.innerText = `Satellite Earth Observation • ${data.name}`;

      const coordsBadge = document.getElementById('geo-coords-badge');
      if (coordsBadge) coordsBadge.innerText = `${data.lat.toFixed(4)}° N, ${data.lng.toFixed(4)}° E`;

      const ndviVal = document.getElementById('geo-ndvi-val');
      if (ndviVal) ndviVal.innerText = data.ndvi_score.toFixed(2);

      const ndviBar = document.getElementById('geo-ndvi-bar');
      if (ndviBar) ndviBar.style.width = `${Math.min(Math.round(data.ndvi_score * 100), 100)}%`;

      const zoneType = document.getElementById('geo-zone-type');
      if (zoneType) zoneType.innerText = data.location_profile.agro_zone || 'Agricultural Belt';

      const statusEl = document.getElementById('geo-feed-status');
      if (statusEl) {
        const t = data.telemetry;
        statusEl.innerText = `Live Telemetry Synchronized: ${t.temperature}°C • ${t.humidity}% Humidity • ${t.rainfall}mm Rain • pH ${t.ph}`;
      }

      const autofillBtnText = document.getElementById('geo-autofill-btn-text');
      if (autofillBtnText) autofillBtnText.innerText = `⚡ Auto-Fill ${data.name.split(',')[0]} Climate into Crop Predictor`;

      // Historical Report Updates
      const historyTitle = document.getElementById('geo-history-title');
      if (historyTitle) historyTitle.innerText = `10-Year Profile: ${data.name}`;

      const zoneBadge = document.getElementById('geo-zone-badge');
      if (zoneBadge) zoneBadge.innerText = data.location_profile.agro_zone.split('(')[0].trim();

      const rainEl = document.getElementById('geo-annual-rain');
      if (rainEl) rainEl.innerText = `${data.historical_telemetry.annual_rainfall_mm} mm`;

      const tempEl = document.getElementById('geo-mean-temp');
      if (tempEl) tempEl.innerText = `${data.historical_telemetry.mean_temperature_c} °C`;

      const soilEl = document.getElementById('geo-soil-type');
      if (soilEl) soilEl.innerText = data.location_profile.soil_type;

      const hazardEl = document.getElementById('geo-hazard-risk');
      if (hazardEl) hazardEl.innerText = data.historical_telemetry.climate_hazard_risk;

      // Recommended Regional Crops
      const cropsContainer = document.getElementById('geo-regional-crops');
      if (cropsContainer && data.location_profile.top_historical_crops) {
        cropsContainer.innerHTML = data.location_profile.top_historical_crops.map(c => `
          <span class="px-2.5 py-1 rounded-lg bg-roast text-almond border border-roast-border text-xs font-mono font-bold capitalize">
            🌱 ${c}
          </span>
        `).join('');
      }

      // Advisory Note
      const noteEl = document.getElementById('geo-advisory-note');
      if (noteEl) noteEl.innerText = data.location_profile.historical_climate_summary || 'Soil and climate conditions align with optimal seasonal crop selection.';

      // ============================================================
      // 1. SATELLITE MULTISPECTRAL INDICES TELEMETRY
      // ============================================================
      const spec = data.spectral_indices || {};
      if (spec.ndvi !== undefined) {
        const el = document.getElementById('spec-ndvi-val');
        if (el) el.innerText = spec.ndvi.toFixed(2);
        const b = document.getElementById('spec-ndvi-badge');
        if (b) b.innerText = spec.ndvi_status || 'High Density';
        const bar = document.getElementById('spec-ndvi-bar');
        if (bar) bar.style.width = `${Math.min(Math.round(spec.ndvi * 100), 100)}%`;
      }
      if (spec.ndwi !== undefined) {
        const el = document.getElementById('spec-ndwi-val');
        if (el) el.innerText = (spec.ndwi > 0 ? '+' : '') + spec.ndwi.toFixed(2);
        const b = document.getElementById('spec-ndwi-badge');
        if (b) b.innerText = spec.ndwi_status || 'Optimal Hydration';
        const bar = document.getElementById('spec-ndwi-bar');
        if (bar) bar.style.width = `${Math.min(Math.round(((spec.ndwi + 1) / 2) * 100), 100)}%`;
      }
      if (spec.evi !== undefined) {
        const el = document.getElementById('spec-evi-val');
        if (el) el.innerText = spec.evi.toFixed(2);
        const b = document.getElementById('spec-evi-badge');
        if (b) b.innerText = spec.evi_status || 'High Vigor';
        const bar = document.getElementById('spec-evi-bar');
        if (bar) bar.style.width = `${Math.min(Math.round(spec.evi * 100), 100)}%`;
      }
      if (spec.soil_moisture_pct !== undefined) {
        const el = document.getElementById('spec-moisture-val');
        if (el) el.innerText = `${spec.soil_moisture_pct}%`;
        const b = document.getElementById('spec-moisture-badge');
        if (b) b.innerText = spec.soil_moisture_status || 'Field Capacity';
        const bar = document.getElementById('spec-moisture-bar');
        if (bar) bar.style.width = `${Math.min(Math.round((spec.soil_moisture_pct / 50) * 100), 100)}%`;
      }

      // ============================================================
      // 2. SOWING CALENDAR & PHENOLOGY UPDATE
      // ============================================================
      const sow = data.sowing_calendar || {};
      const sowStage = document.getElementById('sow-stage-val');
      if (sowStage && sow.stage) sowStage.innerText = sow.stage;
      const sowWin = document.getElementById('sow-window-val');
      if (sowWin && sow.optimal_window) sowWin.innerText = sow.optimal_window;
      const sowCount = document.getElementById('sow-countdown-val');
      if (sowCount && sow.days_to_monsoon !== undefined) {
        sowCount.innerText = `${sow.days_to_monsoon} Days to ${sow.monsoon_name || 'Peak Rainfall'}`;
      }
      const sowWork = document.getElementById('sow-workability-val');
      if (sowWork && sow.soil_workability) sowWork.innerText = sow.soil_workability;

      // ============================================================
      // 3. APMC MANDI LIVE PRICE TICKER
      // ============================================================
      const mandiContainer = document.getElementById('geo-mandi-ticker');
      if (mandiContainer && data.mandi_prices && data.mandi_prices.length > 0) {
        mandiContainer.innerHTML = data.mandi_prices.map(m => `
          <div class="bg-eclipse-surface p-3.5 rounded-xl border border-roast-border relative overflow-hidden group hover:border-almond/50 transition-all">
            <div class="flex items-center justify-between text-[11px] font-mono">
              <span class="text-white font-bold">${m.crop}</span>
              <span class="px-1.5 py-0.5 rounded text-[10px] font-bold ${m.trend.includes('Bullish') || m.trend.includes('Gain') || m.trend.includes('Spike') || m.trend.includes('Rally') ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-roast text-almond border border-almond/20'}">${m.trend}</span>
            </div>
            <div class="mt-2 flex items-baseline justify-between">
              <div class="flex items-baseline space-x-1">
                <span class="text-xs font-bold text-matcha">₹</span>
                <span class="font-sans text-xl font-black text-white">${m.price.toLocaleString('en-IN')}</span>
                <span class="text-[10px] text-mint/60 font-mono">/ Q</span>
              </div>
              <span class="text-xs font-mono font-bold ${m.change.startsWith('+') ? 'text-matcha' : 'text-mint/60'}">${m.change}</span>
            </div>
            <div class="mt-1.5 flex items-center justify-between text-[10px] text-mint/60 font-mono pt-1.5 border-t border-roast-border/50">
              <span>Mandi: ${m.mandi}</span>
              <span>MSP: ₹${m.msp.toLocaleString('en-IN')}</span>
            </div>
          </div>
        `).join('');
      }

      // ============================================================
      // 4. VERIFIED REDDIT, X (TWITTER) & KISAN DISPATCH CARDS
      // ============================================================
      const socialContainer = document.getElementById('geo-social-cards');
      if (socialContainer && data.social_web_feed && data.social_web_feed.length > 0) {
        socialContainer.innerHTML = data.social_web_feed.map(post => `
          <div class="bg-eclipse-surface p-4 rounded-xl border border-roast-border flex flex-col justify-between space-y-3 hover:border-almond/40 transition-all">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${post.badge_class || 'bg-roast text-almond border-almond/30'}">
                    ${post.tag}
                  </span>
                  <span class="text-[10px] font-mono text-mint/70">${post.platform}</span>
                </div>
                <span class="text-[10px] font-mono text-mint/50">${post.timestamp}</span>
              </div>
              <h5 class="font-sans font-bold text-sm text-white leading-snug">${post.title}</h5>
              <p class="text-xs text-mint/80 leading-relaxed">${post.content}</p>
            </div>
            <div class="pt-2.5 border-t border-roast-border/60 flex items-center justify-between text-[10px] font-mono text-mint/70">
              <span class="text-almond font-semibold">${post.handle}</span>
              <span class="text-mint/50">${post.meta}</span>
            </div>
          </div>
        `).join('');
      }
      
      // Refresh Lucide icons for dynamically created DOM elements
      if (window.lucide) {
        window.lucide.createIcons();
      }
    }
  } catch (err) {
    console.error('Geo analysis error:', err);
  }
}

function applyGeoTelemetryToPredictor() {
  if (!currentGeoTelemetry) return;
  const t = currentGeoTelemetry.telemetry;
  if (!t) return;

  const setVal = (key, val) => {
    const s = document.getElementById(`crop-in-${key}`);
    const n = document.getElementById(`crop-num-${key}`);
    if (s) s.value = val;
    if (n) n.value = val;
  };

  setVal('N', t.N);
  setVal('P', t.P);
  setVal('K', t.K);
  setVal('temperature', t.temperature);
  setVal('humidity', t.humidity);
  setVal('ph', t.ph);
  setVal('rainfall', t.rainfall);

  // Switch to Crop Predictor Tab
  switchTab('crop');

  // Execute recommendation immediately with visual feedback
  executeCropPrediction(false);

  // Scroll to top of Crop Predictor smoothly
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================
// INITIALIZATION ON PAGE LOAD
// ============================================================
window.addEventListener('DOMContentLoaded', () => {
  // Execute initial default predictions so the UI is immediately populated
  executeCropPrediction(true);
  executeFertPrediction(true);
  updateCropEconomics();
  updateFertilizerDosage();
  updateCropRotation('rice');
  setTimeout(() => syncSoilReport(), 300);
});

