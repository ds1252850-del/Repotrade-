import React from 'react';
import { Line } from 'react-chartjs-2';

const IndustryBenchmarkChart = ({ industry, data }) => {
  // data: { benchmark, symbols, weights, normalized_prices }
  const chartData = {
    labels: data.symbols,
    datasets: [
      {
        label: `${industry} Normalized Prices`,
        data: data.normalized_prices,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(0, 0, 0, 1)',
        borderWidth: 2,
        fill: false,
        tension: 0.1,
      },
      {
        label: `${industry} Weights`,
        data: data.weights,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 0, 179, 1)',
        borderWidth: 2,
        fill: false,
        tension: 0.1,
        yAxisID: 'y1',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: `${industry} Benchmark` },
    },
    scales: {
      y: { beginAtZero: true, title: { display: true, text: 'Normalized Price' } },
      y1: {
        beginAtZero: true,
        position: 'right',
        title: { display: true, text: 'Weight' },
        grid: { drawOnChartArea: false },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default IndustryBenchmarkChart;
