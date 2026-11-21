// Notificación de cambios por suscripción (variante de MVC de DA-07).
// Los Modelos avisan que cambiaron a quien se haya suscripto, sin saber quién es:
// no conocen a la Vista ni a los Controladores.
export class Observable {
  #suscriptores = new Set()

  // Devuelve la función que cancela la suscripción.
  suscribir(alCambiar) {
    this.#suscriptores.add(alCambiar)
    return () => this.#suscriptores.delete(alCambiar)
  }

  notificar() {
    for (const alCambiar of this.#suscriptores) alCambiar()
  }
}
