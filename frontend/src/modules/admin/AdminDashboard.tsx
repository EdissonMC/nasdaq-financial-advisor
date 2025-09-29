// frontend/src/modules/admin/AdminDashboard.tsx

import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const AdminDashboard = () => {
    const [data, setData] = useState<any>(null);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('http://localhost:8001/admin/dashboard');
            const result = await response.json();
            setData(result);
        };
        fetchData();
    }, []);

    if (!data) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Admin Dashboard</h1>
            
            <h2>Metrics</h2>
            <p>Avg Positive: {data.metrics.avg_positive.toFixed(2)}</p>
            <p>Avg Negative: {data.metrics.avg_negative.toFixed(2)}</p>
            <p>Avg Neutral: {data.metrics.avg_neutral.toFixed(2)}</p>
            <p>Avg Compound: {data.metrics.avg_compound.toFixed(2)}</p>

            <h2>Visualizations</h2>
            <Plot
                data={[
                    {
                        x: data.charts.sentiment_compound,
                        type: 'histogram',
                    },
                ]}
                layout={{ title: 'Distribution of Compound Sentiment' }}
            />
            <Plot
                data={[
                    {
                        x: data.charts.polarity,
                        y: data.charts.subjectivity,
                        mode: 'markers',
                        type: 'scatter',
                        marker: { color: data.charts.sentiment_compound, colorscale: 'Viridis' },
                    },
                ]}
                layout={{ title: 'Polarity vs Subjectivity' }}
            />
            <Plot
                data={[
                    {
                        x: data.charts.created_at,
                        y: data.charts.sentiment_compound,
                        type: 'scatter',
                        mode: 'lines+markers',
                    },
                ]}
                layout={{ title: 'Sentiment Compound Over Time' }}
            />
        </div>
    );
};

export default AdminDashboard;