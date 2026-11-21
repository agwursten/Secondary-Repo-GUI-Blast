import { Observable } from './Observable.js'

// Modelo de resultados: las filas crudas que devolvió el Backend para la tabla.
// En HU11 se le agregan los filtros post-búsqueda, que siempre se calculan desde este crudo.
export class ModeloResultados extends Observable {
  #filas = []
  #cargados = false

  cargar(filas) {
    this.#filas = Object.freeze(filas.map((fila) => Object.freeze({ ...fila })))
    this.#cargados = true
    this.notificar()
  }

  filas() {
    return this.#filas
  }

  cargados() {
    return this.#cargados
  }
}
