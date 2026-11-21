// Cliente del Backend: lo único de la Aplicación Web que conoce la interfaz REST.

// BLAST+ no terminó bien. El mensaje es el literal de BLAST+, sin reinterpretar.
export class ErrorBlast extends Error {
  constructor(mensaje) {
    super(mensaje)
    this.name = 'ErrorBlast'
  }
}

export class ClienteBackend {
  #urlBase

  constructor(urlBase = '') {
    this.#urlBase = urlBase
  }

  // Devuelve las filas de la tabla, o lanza ErrorBlast (o Error si falla la comunicación).
  async ejecutar_busqueda(configuracion) {
    let respuesta
    try {
      respuesta = await fetch(`${this.#urlBase}/api/busquedas/ejecucion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configuracion),
      })
    } catch {
      throw new Error(
        'No se pudo conectar con el servidor de LocalBlast. Verificá que el Backend esté en ejecución.',
      )
    }
    const cuerpo = await respuesta.json().catch(() => null)
    if (respuesta.ok) return cuerpo.filas
    if (cuerpo?.tipo === 'ErrorBlast') throw new ErrorBlast(cuerpo.mensaje)
    throw new Error(
      `El servidor rechazó la solicitud (HTTP ${respuesta.status}).` +
        (cuerpo ? `\n${JSON.stringify(cuerpo.detail ?? cuerpo, null, 2)}` : ''),
    )
  }
}
