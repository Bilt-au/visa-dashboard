import React, { useState, useEffect } from 'react';
import FilterPanel from './components/FilterPanel';
import VisaChart from './components/VisaChart';
import BuyMeACoffeeButton from './components/BuyMeACoffeeButton';
import { apiService } from './services/api';
import { FilterOptions, ChartFilters, VisaDataRecord } from './types/api';
import './App.css';

function App() {
  const [filterOptions, setFilterOptions] = useState<FilterOptions | null>(null);
  const [filters, setFilters] = useState<ChartFilters>({
    eoi_statuses: ['INVITED'] // Default to INVITED status
  });
  const [chartData, setChartData] = useState<VisaDataRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showWelcomeModal, setShowWelcomeModal] = useState(true);

  useEffect(() => {
    loadFilterOptions();
    loadInitialData();

    // Load Buy Me a Coffee script
    const script = document.createElement('script');
    script.src = 'https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js';
    script.setAttribute('data-name', 'bmc-button');
    script.setAttribute('data-slug', 'bilt.au');
    script.setAttribute('data-color', '#FFDD00');
    script.setAttribute('data-emoji', '');
    script.setAttribute('data-font', 'Cookie');
    script.setAttribute('data-text', 'Buy me a coffee');
    script.setAttribute('data-outline-color', '#000000');
    script.setAttribute('data-font-color', '#000000');
    script.setAttribute('data-coffee-color', '#ffffff');

    // Only add if not already present
    if (!document.querySelector('[data-slug="bilt.au"]')) {
      document.head.appendChild(script);
    }
  }, []);

  const loadFilterOptions = async () => {
    try {
      const options = await apiService.getFilterOptions();
      setFilterOptions(options);
    } catch (err) {
      setError('Failed to load filter options. Please check if the backend is running.');
      console.error('Error loading filter options:', err);
    }
  };

  const loadInitialData = async () => {
    // Don't load any data initially - wait for user to apply filters
    setChartData([]);
  };

  const handleApplyFilters = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getVisaData(filters);
      setChartData(response.results);
    } catch (err) {
      setError('Failed to load filtered data. Please try again.');
      console.error('Error loading filtered data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFiltersChange = (newFilters: ChartFilters) => {
    setFilters(newFilters);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🇦🇺 Australian Visa Data Visualization</h1>
        <p>Explore EOI (Expression of Interest) data trends.</p>
        <br></br>
        <BuyMeACoffeeButton className="header-coffee" />
      </header>

      <main className="App-main">
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={() => setError(null)} className="close-error">
              ×
            </button>
          </div>
        )}

        <FilterPanel
          filterOptions={filterOptions}
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onApply={handleApplyFilters}
          loading={loading}
        />

        <div className="chart-section">
          <VisaChart data={chartData} loading={loading} />
        </div>

{chartData.length > 0 && (
          <div className="data-summary">
            <h3>📊 Data Summary</h3>
            <div className="summary-stats">
              <div className="stat">
                <span className="stat-label">Total Records:</span>
                <span className="stat-value">{chartData.length.toLocaleString()}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Unique Visa Types:</span>
                <span className="stat-value">
                  {new Set(chartData.map(d => d.visa_type)).size}
                </span>
              </div>
              <div className="stat">
                <span className="stat-label">Unique Occupations:</span>
                <span className="stat-value">
                  {new Set(chartData.map(d => d.occupation)).size}
                </span>
              </div>
              <div className="stat">
                <span className="stat-label">Total EOI Count:</span>
                <span className="stat-value">
                  {chartData.reduce((sum, d) => sum + d.count_eois, 0).toLocaleString()}
                </span>
              </div>
            </div>
          </div>
        )}

{chartData.length === 0 && (
          <div className="getting-started">
            <h3>🚀 Getting Started</h3>
            <div className="steps">
              <div className="step">
                <span className="step-number">1</span>
                <span className="step-text">Choose your visa types, occupations, points, or status above</span>
              </div>
              <div className="step">
                <span className="step-number">2</span>
                <span className="step-text">Click "Apply Filters & Show Chart"</span>
              </div>
              <div className="step">
                <span className="step-number">3</span>
                <span className="step-text">Analyze the trends and insights</span>
              </div>
            </div>
            <div className="default-status-note">
              <p>💡 <strong>Note:</strong> EOI Status is pre-selected to "INVITED" - the most commonly analyzed status.</p>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <div className="disclaimer">
          <p>
            <strong>Disclaimer:</strong> This dashboard is an independent tool that visualizes publicly available data.
            It is not associated with or endorsed by the Australian Government or Department of Home Affairs.
            This tool is for informational purposes only and should not be used as a substitute for official visa application guidance or advice.
          </p>
        </div>
        <p className="data-source">
            Data sourced from the{' '}
            <a
              href="https://api.dynamic.reports.employment.gov.au/anonap/extensions/hSKLS02_SkillSelect_EOI_Data/hSKLS02_SkillSelect_EOI_Data.html"
              target="_blank"
              rel="noopener noreferrer"
              className="data-source-link"
            >
              SkillSelect Data API
            </a>
          </p>
          <p>Built with ❤️ by <a href="https://www.linkedin.com/in/m4td3v" target="_blank" style={{ color: '#FFF' }}>Matt</a></p>
        
        <br></br>
        <BuyMeACoffeeButton className="footer-coffee" />
      </footer>

      {/* Welcome Modal */}
      {showWelcomeModal && (
        <div className="modal-overlay" onClick={() => setShowWelcomeModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Welcome to the Australian Visa Visualization Dashboard! 🇦🇺</h2>
              <button
                className="modal-close"
                onClick={() => setShowWelcomeModal(false)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <p>
                This dashboard was created <strong>freely</strong> to help analyze EOI (Expression of Interest) trends
                from publicly available SkillSelect data.
              </p>
              <p>
                <strong>Here's what you can do:</strong>
              </p>
              <ul>
                <li>🔍 Filter by visa types, occupations, points, and EOI status</li>
                <li>📊 View interactive charts showing trends over time</li>
                <li>📈 Compare multiple selections simultaneously</li>
                <li>💾 Analyze historical invitation data</li>
              </ul>
              <div className="support-section">
                <p>
                  <strong>💰 Running costs:</strong> While this tool is free, hosting servers and maintaining
                  the data pipeline costs money. If you find this helpful, consider supporting its development!
                </p>
                <div className="modal-actions">
                  <BuyMeACoffeeButton className="coffee-button" />
                  <button
                    className="continue-button"
                    onClick={() => setShowWelcomeModal(false)}
                  >
                    Continue to Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
