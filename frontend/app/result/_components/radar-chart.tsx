'use client';

import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';

/**
 * Register Chart.js components required for radar chart
 * This must be done before using the Radar component
 */
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

/**
 * RadarChartData Interface
 * 
 * Defines the structure of data required for the radar chart visualization.
 * 
 * @property labels - Array of category labels displayed around the radar chart
 * @property datasets - Array of datasets, each representing a data series
 *   - label: Name of the dataset (shown in legend)
 *   - data: Array of numeric values corresponding to each label (0-100 scale)
 *   - backgroundColor: Optional fill color for the radar area
 *   - borderColor: Optional color for the radar line border
 *   - pointBackgroundColor: Optional background color for data points
 *   - pointBorderColor: Optional border color for data points
 *   - pointHoverBackgroundColor: Optional background color on hover
 *   - pointHoverBorderColor: Optional border color on hover
 */
export interface RadarChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor?: string;
    borderColor?: string;
    pointBackgroundColor?: string;
    pointBorderColor?: string;
    pointHoverBackgroundColor?: string;
    pointHoverBorderColor?: string;
  }[];
}

/**
 * Props for the RadarChart component
 */
interface RadarChartProps {
  /** Chart data containing labels and datasets */
  data: RadarChartData;
  /** Optional title displayed above the chart */
  title?: string;
}

/**
 * RadarChart Component
 * 
 * A reusable radar/spider chart component built with Chart.js and react-chartjs-2.
 * Displays multi-dimensional data in a circular radar format, useful for comparing
 * multiple metrics or attributes across different categories.
 * 
 * Features:
 * - Responsive design that adapts to container size
 * - Customizable color scheme (with defaults)
 * - Interactive tooltips on hover
 * - Configurable scale (0-100 by default)
 * - Dark theme optimized styling
 * 
 * @param props - Component props containing chart data and optional title
 * @returns JSX element representing the radar chart
 */
export function RadarChart({ data, title }: RadarChartProps) {
  // Color scheme configuration
  // These colors are optimized for dark theme backgrounds
  const primaryColor = 'rgb(99, 102, 241)'; // Primary accent color (indigo)
  const backgroundColor = 'rgb(2, 15, 25)'; // Dark background for tooltips
  const textColor = 'rgb(200,200,200)'; // Light gray for text elements
  const datasetBackgroundColor = 'rgb(13, 23, 31)'; // Semi-transparent fill for radar area
  const lineColor = 'rgba(200,200,200,0.3)'; // Subtle grid and angle lines

  /**
   * Apply default colors to chart data if not provided
   * This ensures consistent styling while allowing customization
   */
  const chartData = {
    ...data,
    datasets: data.datasets.map((dataset) => ({
      ...dataset,
      backgroundColor: dataset.backgroundColor || datasetBackgroundColor,
      borderColor: dataset.borderColor || primaryColor,
      pointBackgroundColor: dataset.pointBackgroundColor || primaryColor,
      pointBorderColor: dataset.pointBorderColor || backgroundColor,
      pointHoverBackgroundColor: dataset.pointHoverBackgroundColor || backgroundColor,
      pointHoverBorderColor: dataset.pointHoverBorderColor || primaryColor,
    })),
  };

  /**
   * Chart.js configuration options
   * Defines the appearance and behavior of the radar chart
   */
  const options = {
    // Enable responsive behavior to adapt to container size
    responsive: true,
    // Maintain aspect ratio for consistent appearance
    maintainAspectRatio: true,
    plugins: {
      // Legend configuration - displays dataset labels
      legend: {
        position: 'top' as const,
        labels: {
          color: textColor,
          font: {
            size: 14,
          },
        },
      },
      // Tooltip configuration - shows data on hover
      tooltip: {
        enabled: true,
        backgroundColor: backgroundColor,
        titleColor: textColor,
        bodyColor: textColor,
        borderColor: textColor,
        borderWidth: 1,
      },
    },
    scales: {
      // Radial scale configuration (r = radial)
      r: {
        beginAtZero: true, // Start scale from 0
        min: 0, // Minimum value on the scale
        max: 100, // Maximum value on the scale
        ticks: {
          stepSize: 20, // Interval between tick marks (0, 20, 40, 60, 80, 100)
          color: textColor,
          backdropColor: datasetBackgroundColor,
          font: {
            size: 11,
          },
        },
        // Grid lines configuration
        grid: {
          color: lineColor,
        },
        // Point labels (category names around the chart)
        pointLabels: {
          color: textColor,
          font: {
            size: 12,
          },
        },
        // Angle lines (lines from center to each point)
        angleLines: {
          color: lineColor,
        },
      },
    },
    // Visual element styling
    elements: {
      // Line styling (the radar shape outline)
      line: {
        borderWidth: 3,
      },
      // Point styling (data point markers)
      point: {
        radius: 4, // Default point size
        hoverRadius: 6, // Larger size on hover for better interaction feedback
      },
    },
  };

  return (
    <div className="w-full">
      {/* Optional title section */}
      {title && (
        <h3 className="text-xl font-semibold mb-4 text-base-content">{title}</h3>
      )}
      {/* Chart container with fixed height for consistent sizing */}
      <div className="w-full h-[400px] flex items-center justify-center">
        <Radar data={chartData} options={options} />
      </div>
    </div>
  );
}

