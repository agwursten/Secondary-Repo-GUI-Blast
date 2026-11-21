import { Observable } from './Observable.js'

// Estados de la ejecución en el cliente (regla R6 del diseño detallado).
export const Estado = Object.freeze({
  VALIDADA: 'validada',
  EN_EJECUCION: 'en_ejecucion',
  FINALIZADA: 'finalizada',
  CON_ERROR: 'con_error',
})

// Modelo de búsqueda: la configuración validada y el estado de su ejecución.
// Los nombres de las operaciones son los de los diagramas de secuencia.
export class ModeloBusqueda extends Observable {
  #configuracion
  #estado = Estado.VALIDADA
  #mensajeError = null
  #inicio = null
  #fin = null

  // La búsqueda llega ya validada: es la precondición de HU08 (la deja hecha HU05).
  constructor(configuracionValidada) {
    super()
    this.#configuracion = Object.freeze(structuredClone(configuracionValidada))
  }

  configuracion() {
    return this.#configuracion
  }

  estado() {
    return this.#estado
  }

  mensaje_error() {
    return this.#mensajeError
  }

  inicio() {
    return this.#inicio
  }

  fin() {
    return this.#fin
  }

  // Solo se ejecuta una búsqueda validada, o una que terminó con error y se reintenta.
  marcar_en_ejecucion() {
    if (this.#estado !== Estado.VALIDADA && this.#estado !== Estado.CON_ERROR) {
      throw new Error('La búsqueda ya se está ejecutando o ya terminó.')
    }
    this.#estado = Estado.EN_EJECUCION
    this.#mensajeError = null
    this.#inicio = new Date()
    this.#fin = null
    this.notificar()
  }

  marcar_finalizada() {
    this.#estado = Estado.FINALIZADA
    this.#fin = new Date()
    this.notificar()
  }

  registrar_error(mensaje) {
    this.#estado = Estado.CON_ERROR
    this.#mensajeError = mensaje
    this.#fin = new Date()
    this.notificar()
  }
}
