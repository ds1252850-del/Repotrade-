import React, { useEffect, useState } from 'react';
// You may need to install chart.js and react-chartjs-2
import { Line } from 'react-chartjs-2';

const StockScreeningDetail = ({ screeningId }) => {
  const [screening, setScreening] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScreening = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/admin/api/stock-screenings/${screeningId}`);
        const data = await res.json();
        if (data.success) {
          setScreening(data.screening);
        } else {
          setError(data.error || 'Failed to load screening');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchScreening();
  }, [screeningId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!screening) return null;

  const stocks = screening.results_data?.stocks || [];

  return (
    <div>
      <h2>Screening: {screening.name}</h2>
      {stocks.length === 0 && <div>No stocks found in this screening.</div>}
      {stocks.map((stock, idx) => (
        <div key={stock.symbol || idx} style={{ marginBottom: 40, border: '1px solid #eee', padding: 16, borderRadius: 8 }}>
          <h3>{stock.symbol} - {stock.name || stock.company_name}</h3>
          <div>Sector: {stock.sector}</div>
          <div>Price: {stock.price}</div>
          {/* Chart for historical data */}
          {stock.historical_data && stock.historical_data.length > 0 ? (
            <Line
              data={{
                labels: stock.historical_data.map(d => d.date),
                datasets: [
                  {
                    label: 'Close Price',
                    data: stock.historical_data.map(d => d.close),
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                  }
                ]
              }}
              options={{
                responsive: true,
                plugins: {
                  legend: { display: true },
                  title: { display: true, text: `${stock.symbol} Price History` }
                },
                scales: {
                  x: { display: true, title: { display: true, text: 'Date' } },
                  y: { display: true, title: { display: true, text: 'Price' } }
                }
              }}
            />
          ) : (
            <div>No historical data available for chart.</div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StockScreeningDetail;
