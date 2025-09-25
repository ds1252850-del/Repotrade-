import React, { useState } from 'react';
// Chart component import removed
  const [bullishAutomationResult, setBullishAutomationResult] = useState(null);
  const [automationLoading, setAutomationLoading] = useState(false);
  // Automation: Trigger backend bullish stock screening
  const handleBullishAutomation = async () => {
    setAutomationLoading(true);
    setBullishAutomationResult(null);
    // Use all symbols from CSV if available
    let symbols = [];
    if (apiResponse && apiResponse.industry_benchmarks) {
      Object.values(apiResponse.industry_benchmarks).forEach(ind => {
        if (ind.symbols) symbols = symbols.concat(ind.symbols);
      });
    }
    symbols = Array.from(new Set(symbols));
    if (symbols.length === 0) {
      setBullishAutomationResult({ error: 'No symbols found in uploaded CSV.' });
      setAutomationLoading(false);
      return;
    }
    try {
      const res = await fetch('/api/bullish-stocks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbols })
      });
      const data = await res.json();
      setBullishAutomationResult(data);
    } catch (err) {
      setBullishAutomationResult({ error: err.message });
    } finally {
      setAutomationLoading(false);
    }
  };
      {/* Bullish Stock Automation Button */}
      {apiResponse && (
        <div style={{ marginTop: 32, marginBottom: 32 }}>
          <button onClick={handleBullishAutomation} disabled={automationLoading}>
            {automationLoading ? 'Screening for Bullish Stocks...' : 'Run Bullish Stock Automation'}
          </button>
          {bullishAutomationResult && (
            <div style={{ marginTop: 16 }}>
              <h4>Bullish Stocks Result:</h4>
              <pre style={{ background: '#f0f0f0', padding: 10 }}>{JSON.stringify(bullishAutomationResult, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
// Chart component import removed
  const [viewIndustry, setViewIndustry] = useState('');
  // Helper to get industry benchmark data
  const getIndustryBenchmarks = () => {
    if (!apiResponse || !apiResponse.industry_benchmarks) return {};
    return apiResponse.industry_benchmarks;
  };
  // Chart helper removed
  const getAllIndustryNames = () => {
    return Object.keys(getIndustryBenchmarks());
  };
  {/* Charts permanently removed */}

const UserDashboard = ({ initialData }) => {
  const [csvData, setCsvData] = useState(null);
  const [apiResponse, setApiResponse] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [industryType, setIndustryType] = useState('bullish');
  const [selectedIndustry, setSelectedIndustry] = useState('');

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    setApiResponse(null);
    // Preview CSV text
    const reader = new FileReader();
    reader.onload = async (event) => {
      const text = event.target.result;
      setCsvData(text);
      // Send file to backend
      const formData = new FormData();
      formData.append('file', file);
      try {
        const res = await fetch('/api/industry-benchmark', {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        setApiResponse(data);
      } catch (err) {
        setApiResponse({ error: err.message });
      } finally {
        setUploading(false);
      }
    };
    reader.readAsText(file);
  };

  // Helper to get industry list based on type
  const getIndustryList = () => {
    if (!apiResponse) return [];
    if (industryType === 'bullish') return apiResponse.bullish_industries || [];
    if (industryType === 'bearish') return apiResponse.bearish_industries || [];
    return [];
  };

  return (
    <div>
      <h2>User Dashboard</h2>
      <div>
        <label htmlFor="csv-upload">Upload Stock List CSV:</label>
        <input id="csv-upload" type="file" accept=".csv" onChange={handleFileUpload} disabled={uploading} />
        {uploading && <span style={{ marginLeft: 10 }}>Uploading...</span>}
      </div>
      {/* Side Panel: Industry Type Dropdown and Industry Names */}
      {apiResponse && (
        <div style={{ marginTop: 30, border: '1px solid #eee', padding: 16, borderRadius: 8, maxWidth: 400 }}>
          <label htmlFor="industry-type-select" style={{ fontWeight: 'bold' }}>Select Industry Type:</label>
          <select
            id="industry-type-select"
            value={industryType}
            onChange={e => { setIndustryType(e.target.value); setSelectedIndustry(''); }}
            style={{ marginLeft: 10 }}
          >
            <option value="bullish">Bullish</option>
            <option value="bearish">Bearish</option>
          </select>
          <div style={{ marginTop: 16 }}>
            <label htmlFor="industry-select">Industry Names:</label>
            <select
              id="industry-select"
              value={selectedIndustry}
              onChange={e => setSelectedIndustry(e.target.value)}
              style={{ marginLeft: 10 }}
            >
              <option value="">-- Select Industry --</option>
              {getIndustryList().map(ind => (
                <option key={ind} value={ind}>{ind}</option>
              ))}
            </select>
          </div>
        </div>
      )}
      {/* CSV Preview */}
      {csvData && (
        <div style={{ marginTop: 20 }}>
          <h4>CSV Preview (first 500 chars):</h4>
          <pre style={{ maxHeight: 200, overflow: 'auto', background: '#f8f8f8', padding: 10 }}>{csvData.slice(0, 500)}</pre>
        </div>
      )}
      {/* API Response (for debugging, can be removed later) */}
      {apiResponse && (
        <div style={{ marginTop: 20 }}>
          <h4>API Response:</h4>
          <pre style={{ background: '#f0f0f0', padding: 10 }}>{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default UserDashboard;
