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

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

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

interface RadarChartProps {
  data: RadarChartData;
  title?: string;
}

export function RadarChart({ data, title }: RadarChartProps) {
  // Hardcoded colors
  const primaryColor = 'rgb(99, 102, 241)';
  const backgroundColor = 'rgb(2, 15, 25)';
  const textColor = 'rgb(200,200,200)';
  const datasetBackgroundColor = 'rgb(13, 23, 31)';
  const lineColor = 'rgba(200,200,200,0.3)';

  // Apply colors to chart data
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

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: textColor,
          font: {
            size: 14,
          },
        },
      },
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
      r: {
        beginAtZero: true,
        min: 0,
        max: 100,
        ticks: {
          stepSize: 20,
          color: textColor,
          backdropColor: datasetBackgroundColor,
          font: {
            size: 11,
          },
        },
        grid: {
          color: lineColor,
        },
        pointLabels: {
          color: textColor,
          font: {
            size: 12,
          },
        },
        angleLines: {
          color: lineColor,
        },
      },
    },
    elements: {
      line: {
        borderWidth: 3,
      },
      point: {
        radius: 4,
        hoverRadius: 6,
      },
    },
  };

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-xl font-semibold mb-4 text-base-content">{title}</h3>
      )}
      <div className="w-full h-[400px] flex items-center justify-center">
        <Radar data={chartData} options={options} />
      </div>
    </div>
  );
}

