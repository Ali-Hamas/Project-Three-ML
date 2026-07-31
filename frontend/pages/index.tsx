import React, { useState } from 'react';
import axios from 'axios';

interface Entities {
  names: string[];
  organizations: string[];
  locations: string[];
}

interface ExtractionResult {
  success: boolean;
  entities?: Entities;
  inference_time_ms?: number;
  error?: string;
}

export default function Home() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<ExtractionResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleExtract = async () => {
    if (!text.trim()) {
      alert('Please enter some text');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/extract`,
        { text }
      );
      setResult(response.data);
    } catch (error: any) {
      setResult({
        success: false,
        error: error.response?.data?.detail || error.message,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setResult(null);
  };

  return (
    <div style={styles.container}>
      <style>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
          background: linear-gradient(135deg, #001a4d 0%, #003d99 100%);
          min-height: 100vh;
          color: #333;
        }
      `}</style>

      <div style={styles.header}>
        <h1 style={styles.title}>🔍 NER Extraction</h1>
        <p style={styles.subtitle}>Extract entities from text using AI</p>
      </div>

      <div style={styles.card}>
        <div style={styles.section}>
          <label style={styles.label}>Input Text</label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your text here... Example: John Smith works at Google in Mountain View."
            style={styles.textarea}
            disabled={loading}
          />
        </div>

        <div style={styles.buttonGroup}>
          <button
            onClick={handleExtract}
            disabled={loading || !text.trim()}
            style={{
              ...styles.button,
              ...styles.primaryButton,
              opacity: loading || !text.trim() ? 0.6 : 1,
            }}
          >
            {loading ? '⏳ Extracting...' : '✨ Extract Entities'}
          </button>
          <button
            onClick={handleClear}
            disabled={loading}
            style={{
              ...styles.button,
              ...styles.secondaryButton,
            }}
          >
            Clear
          </button>
        </div>

        {result && (
          <div style={styles.resultSection}>
            {result.success ? (
              <>
                <h2 style={styles.resultTitle}>📊 Results</h2>

                <div style={styles.resultGrid}>
                  <div style={styles.resultCard}>
                    <h3 style={styles.entityType}>👤 Names</h3>
                    <div style={styles.entityList}>
                      {result.entities?.names && result.entities.names.length > 0 ? (
                        result.entities.names.map((name, idx) => (
                          <span key={idx} style={styles.entityTag}>
                            {name}
                          </span>
                        ))
                      ) : (
                        <p style={styles.empty}>No names found</p>
                      )}
                    </div>
                  </div>

                  <div style={styles.resultCard}>
                    <h3 style={styles.entityType}>🏢 Organizations</h3>
                    <div style={styles.entityList}>
                      {result.entities?.organizations && result.entities.organizations.length > 0 ? (
                        result.entities.organizations.map((org, idx) => (
                          <span key={idx} style={styles.entityTag}>
                            {org}
                          </span>
                        ))
                      ) : (
                        <p style={styles.empty}>No organizations found</p>
                      )}
                    </div>
                  </div>

                  <div style={styles.resultCard}>
                    <h3 style={styles.entityType}>📍 Locations</h3>
                    <div style={styles.entityList}>
                      {result.entities?.locations && result.entities.locations.length > 0 ? (
                        result.entities.locations.map((loc, idx) => (
                          <span key={idx} style={styles.entityTag}>
                            {loc}
                          </span>
                        ))
                      ) : (
                        <p style={styles.empty}>No locations found</p>
                      )}
                    </div>
                  </div>
                </div>

                <div style={styles.infoBar}>
                  <span>⚡ Inference: {result.inference_time_ms?.toFixed(2)}ms</span>
                </div>
              </>
            ) : (
              <div style={styles.error}>
                <h3>❌ Error</h3>
                <p>{result.error}</p>
              </div>
            )}
          </div>
        )}
      </div>

      <div style={styles.footer}>
        <p>Powered by Qwen2.5-0.5B + LoRA on FastAPI</p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    padding: '40px 20px',
    background: 'linear-gradient(135deg, #001a4d 0%, #003d99 100%)',
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '40px',
    color: 'white',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    marginBottom: '10px',
  },
  subtitle: {
    fontSize: '1.1rem',
    opacity: 0.9,
  },
  card: {
    maxWidth: '900px',
    margin: '0 auto',
    background: 'white',
    borderRadius: '12px',
    padding: '40px',
    boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
  },
  section: {
    marginBottom: '30px',
  },
  label: {
    display: 'block',
    fontSize: '1rem',
    fontWeight: '600',
    marginBottom: '10px',
    color: '#333',
  },
  textarea: {
    width: '100%',
    minHeight: '150px',
    padding: '15px',
    fontSize: '1rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontFamily: 'inherit',
    resize: 'vertical' as const,
    transition: 'border-color 0.3s',
  },
  buttonGroup: {
    display: 'flex',
    gap: '12px',
    marginBottom: '30px',
  },
  button: {
    padding: '12px 24px',
    fontSize: '1rem',
    fontWeight: '600',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  primaryButton: {
    background: 'linear-gradient(135deg, #001a4d 0%, #003d99 100%)',
    color: 'white',
    flex: 1,
  },
  secondaryButton: {
    background: '#f0f0f0',
    color: '#333',
    minWidth: '120px',
  },
  resultSection: {
    marginTop: '40px',
    paddingTop: '30px',
    borderTop: '2px solid #e0e0e0',
  },
  resultTitle: {
    fontSize: '1.5rem',
    fontWeight: '700',
    marginBottom: '20px',
    color: '#333',
  },
  resultGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
    marginBottom: '20px',
  },
  resultCard: {
    padding: '20px',
    background: '#f9f9f9',
    borderRadius: '8px',
    border: '1px solid #e0e0e0',
  },
  entityType: {
    fontSize: '1.1rem',
    fontWeight: '600',
    marginBottom: '15px',
    color: '#001a4d',
  },
  entityList: {
    display: 'flex',
    flexWrap: 'wrap' as const,
    gap: '10px',
  },
  entityTag: {
    background: 'linear-gradient(135deg, #00d4ff 0%, #0099cc 100%)',
    color: 'white',
    padding: '8px 16px',
    borderRadius: '20px',
    fontSize: '0.9rem',
    fontWeight: '500',
  },
  empty: {
    color: '#999',
    fontStyle: 'italic',
  },
  infoBar: {
    padding: '15px',
    background: '#f0f0f0',
    borderRadius: '8px',
    fontSize: '0.95rem',
    color: '#666',
    textAlign: 'center' as const,
  },
  error: {
    padding: '20px',
    background: '#fee',
    borderRadius: '8px',
    border: '1px solid #fcc',
    color: '#c33',
  },
  footer: {
    textAlign: 'center' as const,
    marginTop: '40px',
    color: 'rgba(255, 255, 255, 0.8)',
    fontSize: '0.9rem',
  },
};
