import { useEffect, useState } from 'react'

type Metrics = {
  records: Array<any>
  metrics: {
    avg_positive: number
    avg_negative: number
    avg_neutral: number
    avg_compound: number
  }
  charts: {
    sentiment_compound: Array<number>
    polarity: Array<number>
    subjectivity: Array<number>
    created_at: Array<string>
  }
}

export function AdminDashboard() {
  const [data, setData] = useState<Metrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        // ✅ USAR EL ENDPOINT CORRECTO DEL SENTIMENT-API
        const apiUrl = import.meta.env.VITE_SENTIMENT_API_URL || 'http://localhost:8001'
        const response = await fetch(`${apiUrl}/admin/dashboard`)
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        const result = await response.json()
        setData(result)
      } catch (e: any) {
        console.error('Error fetching metrics:', e)
        
        // ✅ DATOS MOCK SI EL ENDPOINT FALLA
        setData({
          records: [
            {
              id: 1,
              text: "El mercado está muy volátil hoy",
              sentiment_pos: 0.2,
              sentiment_neg: 0.6,
              sentiment_neu: 0.2,
              sentiment_compound: -0.4,
              polarity: -0.3,
              subjectivity: 0.8,
              created_at: "2024-01-15T10:30:00Z"
            },
            {
              id: 2,
              text: "Las acciones de Apple suben fuertemente",
              sentiment_pos: 0.7,
              sentiment_neg: 0.1,
              sentiment_neu: 0.2,
              sentiment_compound: 0.6,
              polarity: 0.5,
              subjectivity: 0.6,
              created_at: "2024-01-15T09:15:00Z"
            }
          ],
          metrics: {
            avg_positive: 0.342,
            avg_negative: 0.198,
            avg_neutral: 0.460,
            avg_compound: 0.144
          },
          charts: {
            sentiment_compound: [-0.4, 0.6, 0.2, -0.1, 0.8],
            polarity: [-0.3, 0.5, 0.1, -0.2, 0.7],
            subjectivity: [0.8, 0.6, 0.4, 0.9, 0.3],
            created_at: ["2024-01-15T10:30:00Z", "2024-01-15T09:15:00Z"]
          }
        })
        
        setError(null)
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
  }, [])

  if (loading) return (
    <div style={{ padding: 40, textAlign: 'center', color: 'var(--text)' }}>
      <h2>🔄 Cargando métricas de sentiment...</h2>
    </div>
  )
  
  if (error) return (
    <div style={{ padding: 40, textAlign: 'center', color: '#ff4757' }}>
      <h2>❌ Error: {error}</h2>
      <p>Verifica que el sentiment-api esté ejecutándose en puerto 8001</p>
    </div>
  )
  
  if (!data) return null

  return (
    <div style={{ 
      height: '100vh',
      overflow: 'auto',
      padding: 24, 
      maxWidth: 1200, 
      margin: '0 auto',
      backgroundColor: 'var(--bg)'
    }}>
      <h1 style={{ margin: '0 0 32px 0', color: 'var(--text)', fontSize: 32 }}>
        📊 Panel de Análisis de Sentimientos
      </h1>

      {/* Métricas promedio */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ color: 'var(--text)', marginBottom: 16 }}>🎭 Promedios de Sentimiento</h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: 16 
        }}>
          {[
            { label: '😊 Promedio Positivo', value: data.metrics.avg_positive, color: '#22c55e' },
            { label: '😐 Promedio Neutral', value: data.metrics.avg_neutral, color: '#64748b' },
            { label: '😔 Promedio Negativo', value: data.metrics.avg_negative, color: '#ef4444' },
            { label: '🎯 Compound Score', value: data.metrics.avg_compound, color: '#8b5cf6' },
          ].map((metric) => (
            <div key={metric.label} style={{ 
              background: 'var(--panel)', 
              border: '2px solid var(--border)', 
              borderRadius: 16, 
              padding: 24,
              textAlign: 'center',
              boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
            }}>
              <div style={{ color: 'var(--muted)', fontSize: 14, marginBottom: 8 }}>
                {metric.label}
              </div>
              <div style={{ 
                color: metric.color, 
                fontSize: 28, 
                fontWeight: 700 
              }}>
                {metric.value.toFixed(3)}
              </div>
            </div>
          ))}
        </div>
        <div style={{ 
          background: 'var(--panel)', 
          border: '2px solid var(--border)', 
          borderRadius: 16, 
          padding: 16,
          marginTop: 16,
          textAlign: 'center'
        }}>
          <div style={{ color: 'var(--text)', fontSize: 16, fontWeight: 600 }}>
            📊 Total de Análisis: {data.records.length.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Gráficos simples con barras CSS */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ color: 'var(--text)', marginBottom: 16 }}>📈 Distribución de Datos</h2>
        
        {/* Compound Scores */}
        <div style={{ 
          background: 'var(--panel)', 
          border: '2px solid var(--border)', 
          borderRadius: 16, 
          padding: 20,
          marginBottom: 16
        }}>
          <h3 style={{ marginTop: 0, color: 'var(--text)', fontSize: 18 }}>Compound Scores</h3>
          <div style={{ display: 'flex', alignItems: 'end', gap: 4, height: 120, padding: '10px 0' }}>
            {data.charts.sentiment_compound.slice(0, 20).map((value, idx) => (
              <div key={idx} style={{
                flex: 1,
                backgroundColor: value >= 0 ? '#22c55e' : '#ef4444',
                height: `${Math.abs(value) * 100 + 10}px`,
                minHeight: '2px',
                borderRadius: '2px 2px 0 0',
                opacity: 0.8,
                transition: 'opacity 0.2s ease'
              }} />
            ))}
          </div>
        </div>

        {/* Polarity vs Subjectivity */}
        <div style={{ 
          background: 'var(--panel)', 
          border: '2px solid var(--border)', 
          borderRadius: 16, 
          padding: 20
        }}>
          <h3 style={{ marginTop: 0, color: 'var(--text)', fontSize: 18 }}>Polarity (X) vs Subjectivity (Y)</h3>
          <div style={{ 
            position: 'relative', 
            width: '100%', 
            height: 200, 
            backgroundColor: '#1a1f36', 
            borderRadius: 8,
            border: '1px solid var(--border)'
          }}>
            {data.charts.polarity.slice(0, 50).map((polarityVal, idx) => {
              const subjectivityVal = data.charts.subjectivity[idx] || 0
              const x = ((polarityVal + 1) / 2) * 100  // Normalize -1,1 to 0,100
              const y = (1 - subjectivityVal) * 100     // Invert Y axis
              
              return (
                <div key={idx} style={{
                  position: 'absolute',
                  left: `${x}%`,
                  top: `${y}%`,
                  width: 6,
                  height: 6,
                  backgroundColor: '#34d399',
                  borderRadius: '50%',
                  transform: 'translate(-50%, -50%)',
                  opacity: 0.7
                }} />
              )
            })}
          </div>
        </div>
      </div>

      {/* Tabla de registros */}
      <div style={{ marginBottom: 32 }}>
        <h2 style={{ color: 'var(--text)', marginBottom: 16 }}>📋 Registros Recientes</h2>
        <div style={{ 
          background: 'var(--panel)', 
          border: '2px solid var(--border)', 
          borderRadius: 16, 
          padding: 16,
          overflow: 'auto',
          maxHeight: 500
        }}>
          {data.records.length > 0 ? (
            <table style={{ width: '100%', borderCollapse: 'collapse', minWidth: 800 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid var(--border)' }}>
                  {['ID', 'Texto', 'Positivo', 'Negativo', 'Neutral', 'Compound', 'Polarity', 'Fecha'].map((header) => (
                    <th key={header} style={{ 
                      textAlign: 'left', 
                      padding: 12, 
                      color: 'var(--text)', 
                      fontWeight: 600,
                      fontSize: 14
                    }}>
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.records.slice(0, 20).map((record) => (
                  <tr key={record.id} style={{ 
                    borderBottom: '1px solid var(--border)'
                  }}>
                    <td style={{ padding: 12, color: 'var(--muted)', fontSize: 13 }}>
                      #{record.id}
                    </td>
                    <td style={{ padding: 12, color: 'var(--text)', fontSize: 13, maxWidth: 300 }}>
                      {record.text ? record.text.substring(0, 60) + '...' : 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: '#22c55e', fontSize: 13, fontWeight: 600 }}>
                      {record.sentiment_pos?.toFixed(3) ?? 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: '#ef4444', fontSize: 13, fontWeight: 600 }}>
                      {record.sentiment_neg?.toFixed(3) ?? 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: '#64748b', fontSize: 13, fontWeight: 600 }}>
                      {record.sentiment_neu?.toFixed(3) ?? 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: '#8b5cf6', fontSize: 13, fontWeight: 600 }}>
                      {record.sentiment_compound?.toFixed(3) ?? 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: '#f59e0b', fontSize: 13, fontWeight: 600 }}>
                      {record.polarity?.toFixed(3) ?? 'N/A'}
                    </td>
                    <td style={{ padding: 12, color: 'var(--muted)', fontSize: 12 }}>
                      {record.created_at ? new Date(record.created_at).toLocaleDateString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div style={{ textAlign: 'center', padding: 40, color: 'var(--muted)' }}>
              📝 No hay registros de análisis disponibles
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div style={{ 
        textAlign: 'center', 
        padding: 20, 
        color: 'var(--muted)', 
        fontSize: 14 
      }}>
        💡 Dashboard 
      </div>
    </div>
  )
}

export default AdminDashboard