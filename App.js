import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [userId, setUserId] = useState('');
  const [purposes, setPurposes] = useState([]);
  const [consents, setConsents] = useState({});
  const [showBanner, setShowBanner] = useState(true);
  const [showPreferences, setShowPreferences] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [activeTab, setActiveTab] = useState('consent');

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      setLoading(true);
      // Initialize or retrieve user ID
      let storedUserId = Cookies.get('user_id');
      if (!storedUserId) {
        storedUserId = uuidv4();
        Cookies.set('user_id', storedUserId, { expires: 365 });
      }
      setUserId(storedUserId);

      // Fetch purposes and consents
      await Promise.all([
        fetchPurposes(),
        fetchConsents(storedUserId),
        fetchStats()
      ]);
    } catch (error) {
      setError('Failed to initialize application');
      console.error('Initialization error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPurposes = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/purposes`);
      setPurposes(response.data);
    } catch (error) {
      console.error('Error fetching purposes:', error);
      setError('Failed to load consent purposes');
    }
  };

  const fetchConsents = async (uid) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/consent?user_id=${uid}`);
      const consentMap = {};
      response.data.forEach(consent => {
        consentMap[consent.purpose_id] = consent.status;
      });
      setConsents(consentMap);
    } catch (error) {
      console.error('Error fetching consents:', error);
      setError('Failed to load your consent preferences');
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/consent/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const updateConsent = async (purposeId, status) => {
    try {
      await axios.post(`${API_BASE_URL}/api/consent`, {
        user_id: userId,
        purpose_id: purposeId,
        status: status
      });
      setConsents(prev => ({ ...prev, [purposeId]: status }));
      
      // Refresh stats after consent update
      fetchStats();
    } catch (error) {
      console.error('Error updating consent:', error);
      setError('Failed to update consent preference');
    }
  };

  const handleBulkUpdate = async (status) => {
    try {
      const consentsData = purposes.map(purpose => ({
        purpose_id: purpose.id,
        status: status
      }));

      await axios.post(`${API_BASE_URL}/api/consent/bulk`, {
        user_id: userId,
        consents: consentsData
      });

      const newConsents = {};
      purposes.forEach(purpose => {
        newConsents[purpose.id] = status;
      });
      setConsents(newConsents);
      
      // Refresh stats
      fetchStats();
    } catch (error) {
      console.error('Error bulk updating consents:', error);
      setError('Failed to update consent preferences');
    }
  };

  const handleAcceptAll = () => {
    handleBulkUpdate(true);
    setShowBanner(false);
  };

  const handleRejectAll = () => {
    handleBulkUpdate(false);
    setShowBanner(false);
  };

  const handleSavePreferences = () => {
    setShowPreferences(false);
    setShowBanner(false);
  };

  const getConsentStatus = (purposeId) => {
    return consents[purposeId] !== undefined ? consents[purposeId] : null;
  };

  const getConsentStatusText = (purposeId) => {
    const status = getConsentStatus(purposeId);
    if (status === null) return 'Not set';
    return status ? 'Allowed' : 'Denied';
  };

  const getPurposeIcon = (purposeName) => {
    const name = purposeName.toLowerCase();
    if (name.includes('analytics') || name.includes('statistics')) return '📊';
    if (name.includes('marketing') || name.includes('advertising')) return '🎯';
    if (name.includes('essential') || name.includes('necessary')) return '⚡';
    if (name.includes('functional') || name.includes('features')) return '🔧';
    if (name.includes('social') || name.includes('media')) return '📱';
    if (name.includes('performance') || name.includes('speed')) return '🚀';
    return '🔐';
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>✨ Loading your privacy preferences...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>⚠️ Oops! Something went wrong</h2>
        <p>{error}</p>
        <button className="btn-primary" onClick={initializeApp}>🔄 Try Again</button>
      </div>
    );
  }

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>Privacy Consent Manager</h1>
          <div className="header-actions">
            <button 
              className="btn-secondary"
              onClick={() => setShowDashboard(!showDashboard)}
            >
              {showDashboard ? '📊 Hide Dashboard' : '📊 Show Dashboard'}
            </button>
            <button 
              className="btn-secondary"
              onClick={() => setShowPreferences(true)}
            >
              ⚙️ Manage Preferences
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {showDashboard && (
          <div className="dashboard">
            <div className="dashboard-header">
              <h2>Privacy Analytics Dashboard</h2>
              <div className="tab-buttons">
                <button 
                  className={`tab-btn ${activeTab === 'consent' ? 'active' : ''}`}
                  onClick={() => setActiveTab('consent')}
                >
                  🔐 Consent Overview
                </button>
                <button 
                  className={`tab-btn ${activeTab === 'stats' ? 'active' : ''}`}
                  onClick={() => setActiveTab('stats')}
                >
                  📈 Statistics
                </button>
              </div>
            </div>

            {activeTab === 'consent' && (
              <div className="consent-overview">
                <div className="consent-grid">
                  {purposes.map(purpose => (
                    <div key={purpose.id} className="consent-card">
                      <div className="consent-card-header">
                        <h3>{getPurposeIcon(purpose.name)} {purpose.name}</h3>
                        <span className={`status-badge ${getConsentStatus(purpose.id) ? 'allowed' : 'denied'}`}>
                          {getConsentStatus(purpose.id) ? '✅ Allowed' : '❌ Denied'}
                        </span>
                      </div>
                      <p>{purpose.description}</p>
                      <div className="consent-card-actions">
                        <button 
                          className={`btn-toggle ${getConsentStatus(purpose.id) ? 'active' : ''}`}
                          onClick={() => updateConsent(purpose.id, !getConsentStatus(purpose.id))}
                        >
                          {getConsentStatus(purpose.id) ? '✅ Allowed' : '❌ Denied'}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'stats' && stats && (
              <div className="stats-overview">
                <div className="stats-grid">
                  <div className="stat-card">
                    <h3>📊 Total Consents</h3>
                    <div className="stat-value">{stats.total_consents}</div>
                  </div>
                  <div className="stat-card">
                    <h3>✅ Active Consents</h3>
                    <div className="stat-value">{stats.active_consents}</div>
                  </div>
                  <div className="stat-card">
                    <h3>📈 Consent Rate</h3>
                    <div className="stat-value">{stats.consent_rate.toFixed(1)}%</div>
                  </div>
                </div>
                
                <div className="purpose-stats">
                  <h3>📊 Consent by Purpose</h3>
                  <div className="purpose-stats-list">
                    {stats.by_purpose.map((purpose, index) => (
                      <div key={index} className="purpose-stat-item">
                        <div className="purpose-stat-info">
                          <span className="purpose-name">{getPurposeIcon(purpose.purpose_name)} {purpose.purpose_name}</span>
                          <span className="purpose-rate">{purpose.rate.toFixed(1)}%</span>
                        </div>
                        <div className="progress-bar">
                          <div 
                            className="progress-fill" 
                            style={{ width: `${purpose.rate}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Demo Content */}
        <div className="demo-content">
          <h2>🌟 Welcome to Your Privacy Hub</h2>
          <p>Take control of your digital privacy with our advanced consent management system. Every choice you make helps create a more transparent and secure online experience.</p>
          
          <div className="demo-features">
            <div className="feature">
              <h3>🔒 Privacy First</h3>
              <p>Your consent preferences are stored securely with enterprise-grade encryption. You have complete control over your data and can change your preferences anytime.</p>
            </div>
            <div className="feature">
              <h3>📊 Complete Transparency</h3>
              <p>View detailed analytics about consent rates, understand how your data is used, and make informed decisions about your privacy with our comprehensive dashboard.</p>
            </div>
            <div className="feature">
              <h3>⚡ Instant Control</h3>
              <p>Update your consent preferences with just a few clicks. Our intuitive interface makes managing your privacy simple, fast, and hassle-free.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Consent Banner */}
      {showBanner && (
        <div className="consent-banner">
          <div className="banner-content">
            <div className="banner-text">
              <h3>🍪 Cookie & Privacy Consent</h3>
              <p>We use cookies and similar technologies to enhance your experience, analyze usage patterns, and personalize content. Your privacy matters to us - please review and manage your preferences below.</p>
            </div>
            <div className="banner-actions">
              <button className="btn-primary" onClick={handleAcceptAll}>
                ✅ Accept All
              </button>
              <button className="btn-secondary" onClick={handleRejectAll}>
                ❌ Reject All
              </button>
              <button className="btn-outline" onClick={() => setShowPreferences(true)}>
                ⚙️ Manage Preferences
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Preferences Modal */}
      {showPreferences && (
        <div className="modal-overlay" onClick={() => setShowPreferences(false)}>
          <div className="preferences-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>⚙️ Manage Privacy Preferences</h2>
              <button className="close-btn" onClick={() => setShowPreferences(false)}>×</button>
            </div>
            
            <div className="preferences-content">
              <div className="preferences-list">
                {purposes.map(purpose => (
                  <div key={purpose.id} className="preference-item">
                    <div className="preference-info">
                      <h3>{getPurposeIcon(purpose.name)} {purpose.name}</h3>
                      <p>{purpose.description}</p>
                    </div>
                    <div className="preference-control">
                      <label className="toggle-switch">
                        <input
                          type="checkbox"
                          checked={getConsentStatus(purpose.id) || false}
                          onChange={(e) => updateConsent(purpose.id, e.target.checked)}
                        />
                        <span className="toggle-slider"></span>
                      </label>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="modal-actions">
                <button className="btn-secondary" onClick={() => setShowPreferences(false)}>
                  ❌ Cancel
                </button>
                <button className="btn-primary" onClick={handleSavePreferences}>
                  ✅ Save Preferences
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App; 