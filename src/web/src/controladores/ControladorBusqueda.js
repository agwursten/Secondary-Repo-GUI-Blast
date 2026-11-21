// Controlador de búsqueda: interpreta la acción "ejecutar" del investigador.
// Sigue las Secuencias 1 y 2 del diseño detallado. Cambia los Modelos; la Vista se
// entera del cambio porque los observa (DA-07), no porque el Controlador la llame.
export class ControladorBusqueda {
  #modeloBusqueda
  #modeloResultados
  #cliente

  constructor(modeloBusqueda, modeloResultados, cliente) {
    this.#modeloBusqueda = modeloBusqueda
    this.#modeloResultados = modeloResultados
    this.#cliente = cliente
  }

  // La llamada al Backend es asíncrona: mientras espera, la interfaz sigue navegable (CA-01).
  async ejecutar() {
    const configuracion = this.#modeloBusqueda.configuracion()
    this.#modeloBusqueda.marcar_en_ejecucion()
    try {
      const filas = await this.#cliente.ejecutar_busqueda(configuracion)
      this.#modeloResultados.cargar(filas)
      this.#modeloBusqueda.marcar_finalizada()
    } catch (error) {
      this.#modeloBusqueda.registrar_error(error.message)
    }
  }
}
