// Formato de los números para mostrarlos. Es presentación, no regla del negocio.

export function formatearEvalue(evalue) {
  if (evalue === 0) return '0.0'
  if (evalue < 0.001) return evalue.toExponential(0)
  return Number(evalue.toPrecision(2)).toString()
}

export function formatearScore(score) {
  return score.toFixed(1)
}

export function formatearPorcentaje(valor) {
  return `${valor.toFixed(1)}%`
}

export function formatearHora(fecha) {
  return fecha ? fecha.toLocaleTimeString('es-AR', { hour12: false }) : '—'
}

export function formatearDuracion(milisegundos) {
  const segundos = Math.max(0, Math.floor(milisegundos / 1000))
  const minutos = Math.floor(segundos / 60)
  return `${String(minutos).padStart(2, '0')}:${String(segundos % 60).padStart(2, '0')}`
}
