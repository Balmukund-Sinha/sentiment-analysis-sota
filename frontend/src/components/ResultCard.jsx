
import React from 'react';

const ResultCard = ({ result }) => {
    if (!result) {
        return (
            <div className="glass-panel" style={{ padding: '2rem', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: 'var(--text-muted)' }}>
                <p>Awaiting Analysis...</p>
            </div>
        );
    }

    const isPositive = result.sentiment === 'Positive';
    const isNeutral = result.sentiment === 'Neutral';
    const isNegative = result.sentiment === 'Negative';
    const confidencePercent = Math.round(result.confidence * 100);
    const isReliable = result.status === 'Reliable';

    return (
        <div className="glass-panel action-card result-card-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
                <span className="subtitle">Prediction Result</span>
                <span className="subtitle" style={{ fontSize: '0.8rem' }}>Model: {result.model_version}</span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', marginBottom: '2rem' }}>
                <div className={`result-label ${isPositive ? 'result-positive' : (isNeutral ? 'result-neutral' : 'result-negative')}`} style={{ fontSize: '2rem' }}>
                    {result.sentiment}
                    <span className={`badge ${isReliable ? 'badge-reliable' : 'badge-uncertain'}`} style={{ marginLeft: '1rem', fontSize: '0.7rem' }}>
                        {result.status}
                    </span>
                </div>

                <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
                        <span>Confidence</span>
                        <span style={{ fontWeight: '800' }}>{confidencePercent}%</span>
                    </div>
                    <div className="confidence-bg">
                        <div
                            className="confidence-fill"
                            style={{
                                width: `${confidencePercent}%`,
                                backgroundColor: isPositive ? 'var(--success)' : (isNeutral ? '#eab308' : 'var(--danger)')
                            }}
                        />
                    </div>
                </div>
            </div>

            <div style={{ padding: '1rem', background: 'rgba(150,150,150,0.05)', borderRadius: '12px', marginBottom: '2rem' }}>
                <div style={{ marginBottom: '0.5rem', fontSize: '0.85rem', fontWeight: 'bold' }}>Probability Distribution:</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
                    <div style={{ borderLeft: '4px solid var(--success)', paddingLeft: '8px' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Positive</div>
                        <div style={{ fontWeight: '800' }}>{Math.round((result.probabilities.positive || 0) * 100)}%</div>
                    </div>
                    <div style={{ borderLeft: '4px solid #eab308', paddingLeft: '8px' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Neutral</div>
                        <div style={{ fontWeight: '800' }}>{Math.round((result.probabilities.neutral || 0) * 100)}%</div>
                    </div>
                    <div style={{ borderLeft: '4px solid var(--danger)', paddingLeft: '8px' }}>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Negative</div>
                        <div style={{ fontWeight: '800' }}>{Math.round((result.probabilities.negative || 0) * 100)}%</div>
                    </div>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.75rem', borderTop: '1px solid rgba(150,150,150,0.1)', paddingTop: '0.5rem' }}>
                    ⚡ Latency: {result.latency_ms}ms • Model: {result.model_version}
                </div>
            </div>

            {result.explanation && (
                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h4 style={{ fontWeight: '700' }}>Model Evidence (SHAP)</h4>
                        <div style={{ display: 'flex', gap: '0.75rem', fontSize: '0.7rem' }}>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                <div style={{ width: 8, height: 8, background: 'rgba(0, 120, 255, 0.6)', borderRadius: '2px' }}></div> Positive
                            </span>
                             <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                <div style={{ width: 8, height: 8, background: 'rgba(234, 179, 8, 0.6)', borderRadius: '2px' }}></div> Neutral
                            </span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                <div style={{ width: 8, height: 8, background: 'rgba(255, 60, 60, 0.6)', borderRadius: '2px' }}></div> Negative
                            </span>
                        </div>
                    </div>

                    <div style={{ lineHeight: '2', fontSize: '1.05rem' }}>
                        {result.explanation.map((item, idx) => {
                            const val = item.normalized_score || 0;
                            const isPos = val > 0;
                            const opacity = Math.abs(val) * 0.7;
                            let color = `rgba(150, 150, 150, ${opacity})`; // Neutralish grey if near 0
                            
                            if (isPositive) {
                                color = isPos ? `rgba(0, 120, 255, ${opacity})` : `rgba(255, 60, 60, ${opacity})`;
                            } else if (isNeutral) {
                                color = isPos ? `rgba(234, 179, 8, ${opacity})` : `rgba(200, 200, 200, ${opacity})`;
                            } else if (isNegative) {
                                color = isPos ? `rgba(0, 120, 255, ${opacity})` : `rgba(255, 60, 60, ${opacity})`;
                            }

                            return (
                                <span
                                    key={idx}
                                    data-tooltip={`Impact: ${(item.score * 100).toFixed(2)}`}
                                    style={{
                                        backgroundColor: color,
                                        padding: '2px 0px',
                                        borderRadius: '2px',
                                        display: 'inline-block',
                                        whiteSpace: 'pre-wrap',
                                        minWidth: item.token === ' ' ? '0.5em' : 'auto',
                                        borderBottom: opacity > 0.2 ? `2px solid ${isPos ? '#0078FF' : '#FF3C3C'}` : 'none'
                                    }}
                                >
                                    {item.token || '\u00A0'}
                                </span>
                            );
                        })}
                    </div>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '1rem', fontStyle: 'italic' }}>
                        *Hover over words to see exact contribution values.
                    </p>
                </div>
            )}
        </div>
    );
};

export default ResultCard;
