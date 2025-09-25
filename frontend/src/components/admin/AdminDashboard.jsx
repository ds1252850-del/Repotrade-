import React, { useEffect, useState } from 'react';
import StockScreeningDetail from './StockScreeningDetail';

const AdminDashboard = () => {
  const [screenings, setScreenings] = useState([]);
  const [selectedScreeningId, setSelectedScreeningId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScreenings = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch('/admin/api/stock-screenings');
        const data = await res.json();
        if (data.success) {
          setScreenings(data.screenings || []);
        } else {
          setError(data.error || 'Failed to load screenings');
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchScreenings();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  if (selectedScreeningId) {
    return (
      <div>
        <button onClick={() => setSelectedScreeningId(null)} style={{ marginBottom: 16 }}>Back to Screenings</button>
        <StockScreeningDetail screeningId={selectedScreeningId} />
      </div>
    );
  }

  return (
    <div>
      <h2>Stock Screenings</h2>
      {screenings.length === 0 && <div>No screenings found.</div>}
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Name</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Date</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Count</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {screenings.map(screening => (
            <tr key={screening.id}>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{screening.name}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{screening.created_at}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{screening.count}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>
                <button onClick={() => setSelectedScreeningId(screening.id)}>View</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
