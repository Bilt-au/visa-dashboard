import React, { useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { VisaDataRecord } from '../types/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface VisaChartProps {
  data: VisaDataRecord[];
  loading: boolean;
}

const VisaChart: React.FC<VisaChartProps> = ({ data, loading }) => {
  const [showTable, setShowTable] = useState(false);
  if (loading) {
    return <div className="chart-container loading">Loading chart...</div>;
  }

  if (!data || data.length === 0) {
    return (
      <div className="chart-container empty">
        <div>
          <h3>🎯 Ready to Explore Your Data</h3>
          <p>Select your preferred filters above and click "Apply Filters" to view the trends.</p>
          <p>💡 <strong>Tip:</strong> You can select multiple options in each filter for comprehensive analysis!</p>
        </div>
      </div>
    );
  }

  // Generate colors for different lines
  const colors = [
    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
    '#FF9F40', '#C9CBCF', '#FF6384', '#36A2EB', '#FFCE56'
  ];

  // Group data by unique combination of visa_type, occupation, points, and status
  const groupedData = data.reduce((acc, record) => {
    const key = `${record.visa_type} - ${record.occupation} - ${record.points} pts - ${record.eoi_status}`;
    if (!acc[key]) {
      acc[key] = [];
    }
    acc[key].push(record);
    return acc;
  }, {} as Record<string, VisaDataRecord[]>);

  // Get all unique month_years and sort them
  const allMonthYears = Array.from(new Set(data.map(record => record.month_year)))
    .sort((a, b) => new Date(a).getTime() - new Date(b).getTime());

  // Create datasets for each group
  const datasets = Object.entries(groupedData).map(([key, records], index) => {
    // Create data points for each month_year
    const dataPoints = allMonthYears.map(monthYear => {
      const record = records.find(r => r.month_year === monthYear);
      return record ? record.count_eois : 0;
    });

    return {
      label: key,
      data: dataPoints,
      borderColor: colors[index % colors.length],
      backgroundColor: colors[index % colors.length] + '20',
      borderWidth: 2,
      fill: false,
      tension: 0.1,
      pointRadius: 4,
      pointHoverRadius: 6,
    };
  });

  const chartData = {
    labels: allMonthYears.map(monthYear =>
      new Date(monthYear).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short'
      })
    ),
    datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: 'EOI Count Over Time',
        font: {
          size: 16,
          weight: 'bold' as const,
        }
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
        cornerRadius: 8,
        padding: 12,
        position: 'nearest' as const,
        xAlign: 'center' as const,
        yAlign: 'top' as const,
        caretPadding: 10,
        displayColors: true,
        bodySpacing: 4,
        titleSpacing: 2,
        titleMarginBottom: 8,
        filter: function(tooltipItem: any) {
          return tooltipItem.parsed.y !== null && tooltipItem.parsed.y > 0;
        },
        callbacks: {
          title: function(context: any) {
            return context && context.length > 0 && context[0] ? context[0].label : '';
          },
          label: function(context: any) {
            const label = context?.dataset?.label || '';
            const value = context?.parsed?.y || 0;
            return `${label}: ${value} EOIs`;
          },
          afterBody: function() {
            return ['', '⚠️ Note: Values <20 are considered as 0'];
          }
        }
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Month Year',
          font: {
            size: 14,
            weight: 'bold' as const,
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'EOI Count',
          font: {
            size: 14,
            weight: 'bold' as const,
          }
        },
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        }
      },
    },
    interaction: {
      mode: 'nearest' as const,
      axis: 'x' as const,
      intersect: false,
    },
  };

  return (
    <div className="chart-container">
      <div className="chart-wrapper">
        <Line data={chartData} options={options} />
      </div>
      <div className="chart-info">
        <p>Showing {datasets.length} data series with {data.length} total records</p>
        <button
          onClick={() => setShowTable(!showTable)}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            backgroundColor: '#36A2EB',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          {showTable ? '▲ Hide Data Table' : '▼ Show Data Table'}
        </button>
      </div>

      {showTable && (
        <div className="data-table-container" style={{ marginTop: '20px', overflowX: 'auto' }}>
          <h4 style={{ marginBottom: '10px' }}>Chart Data Values</h4>
          <table style={{
            width: '100%',
            borderCollapse: 'collapse',
            fontSize: '12px',
            border: '1px solid #ddd'
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ padding: '8px', border: '1px solid #ddd', textAlign: 'left' }}>
                  Series
                </th>
                {allMonthYears.map(monthYear => (
                  <th key={monthYear} style={{
                    padding: '8px',
                    border: '1px solid #ddd',
                    textAlign: 'center',
                    minWidth: '80px'
                  }}>
                    {new Date(monthYear).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short'
                    })}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {datasets.map((dataset, index) => (
                <tr key={index} style={{
                  backgroundColor: index % 2 === 0 ? 'white' : '#f9f9f9'
                }}>
                  <td style={{
                    padding: '8px',
                    border: '1px solid #ddd',
                    fontWeight: 'bold',
                    maxWidth: '200px',
                    wordBreak: 'break-word'
                  }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px'
                    }}>
                      <div style={{
                        width: '12px',
                        height: '12px',
                        backgroundColor: dataset.borderColor,
                        borderRadius: '2px'
                      }}></div>
                      {dataset.label}
                    </div>
                  </td>
                  {dataset.data.map((value, valueIndex) => (
                    <td key={valueIndex} style={{
                      padding: '8px',
                      border: '1px solid #ddd',
                      textAlign: 'center'
                    }}>
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <p style={{
            fontSize: '11px',
            color: '#666',
            marginTop: '10px',
            fontStyle: 'italic'
          }}>
            ⚠️ Note: Values &lt;20 are considered as 0
          </p>
        </div>
      )}
    </div>
  );
};

export default VisaChart;