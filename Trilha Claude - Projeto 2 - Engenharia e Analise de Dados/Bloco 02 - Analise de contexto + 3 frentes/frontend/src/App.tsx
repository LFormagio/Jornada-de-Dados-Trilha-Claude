import React from 'react';
import { motion } from 'framer-motion';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';
import { BarChart3, Database } from 'lucide-react';
import { useQuery } from './hooks/useQuery';
import { Card, CardHeader, CardContent } from './components/Card';

import './index.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

ChartJS.defaults.color = '#a1a1aa';
ChartJS.defaults.font.family = "'Inter', sans-serif";

interface Payload {
  generation_date: string;
  kpis: { faturamento_total: number; ticket_medio: number; vendas_totais: number; clientes_ativos: number };
  charts: { categories: { labels: string[], values: number[] }, channels: { labels: string[], values: number[] } };
  competitors: Array<{ nome: string; nosso_preco: number; media_mercado: number; status: string; badge_class: string; margem_dif: number }>;
}

function App() {
  const { data, loading, error } = useQuery<Payload>('dashboard_data', '/data_payload.json');

  if (loading) return <div style={{ padding: '2rem' }}>Carregando dados executivos...</div>;
  if (error || !data) return <div style={{ padding: '2rem', color: '#ef4444' }}>Erro ao carregar os dados. Rode python scripts/build_app.py primeiro.</div>;

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <div className="brand">
          <BarChart3 size={24} /> DataDash
        </div>
        <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem', marginTop: 'auto' }}>
          Gerado em:<br />
          <span style={{ color: 'var(--color-text-primary)', fontWeight: 500 }}>{data.generation_date}</span>
        </div>
      </aside>

      <main className="main-content">
        <div className="top-bar">
          <h1 className="page-title">Visão Geral Executiva</h1>
        </div>

        <motion.section 
          className="kpi-grid"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: { opacity: 0 },
            visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
          }}
        >
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
            <Card>
              <CardHeader>Faturamento Total</CardHeader>
              <CardContent>
                <div className="kpi-value">R$ {data.kpis.faturamento_total.toLocaleString()}</div>
                <div className="trend-positive">+ Performance Geral</div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
            <Card>
              <CardHeader>Ticket Médio</CardHeader>
              <CardContent>
                <div className="kpi-value">R$ {data.kpis.ticket_medio.toLocaleString()}</div>
                <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem' }}>Por compra</div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
            <Card>
              <CardHeader>Volume Vendas</CardHeader>
              <CardContent>
                <div className="kpi-value">{data.kpis.vendas_totais.toLocaleString()}</div>
                <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem' }}>Transações concluídas</div>
              </CardContent>
            </Card>
          </motion.div>
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}>
            <Card>
              <CardHeader>Clientes Ativos</CardHeader>
              <CardContent>
                <div className="kpi-value">{data.kpis.clientes_ativos.toLocaleString()}</div>
                <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.85rem' }}>Na base de dados</div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.section>

        <section className="charts-grid">
          <Card>
            <CardHeader>Faturamento por Categoria</CardHeader>
            <CardContent>
              <div style={{ height: '300px' }}>
                <Bar 
                  data={{
                    labels: data.charts.categories.labels,
                    datasets: [{
                      label: 'Faturamento (R$)',
                      data: data.charts.categories.values,
                      backgroundColor: 'rgba(79, 209, 197, 0.8)',
                      borderRadius: 6
                    }]
                  }}
                  options={{ responsive: true, maintainAspectRatio: false }}
                />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>Share de Canais</CardHeader>
            <CardContent>
              <div style={{ height: '300px' }}>
                <Doughnut 
                  data={{
                    labels: data.charts.channels.labels,
                    datasets: [{
                      data: data.charts.channels.values,
                      backgroundColor: ['rgba(99, 102, 241, 0.8)', 'rgba(79, 209, 197, 0.8)', 'rgba(16, 185, 129, 0.8)'],
                      borderWidth: 0
                    }]
                  }}
                  options={{ responsive: true, maintainAspectRatio: false, cutout: '70%' }}
                />
              </div>
            </CardContent>
          </Card>
        </section>

        <motion.section 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="table-section">
            <CardHeader>Análise de Concorrência (Top 5)</CardHeader>
            <CardContent>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>Nosso Preço</th>
                    <th>Média Mercado</th>
                    <th>Status</th>
                    <th>Margem</th>
                  </tr>
                </thead>
                <tbody>
                  {data.competitors.map((row, i) => (
                    <tr key={i}>
                      <td><strong>{row.nome}</strong></td>
                      <td>R$ {row.nosso_preco.toFixed(2)}</td>
                      <td>R$ {row.media_mercado.toFixed(2)}</td>
                      <td><span className={`badge ${row.badge_class}`}>{row.status}</span></td>
                      <td className={row.badge_class}>{row.margem_dif.toFixed(1)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </CardContent>
          </Card>
        </motion.section>
      </main>
    </div>
  );
}

export default App;
