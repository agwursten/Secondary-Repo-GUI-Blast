import { useEffect, useReducer } from 'react'

// La Vista se suscribe a un Modelo y se vuelve a dibujar cada vez que cambia.
// Solo lee: nunca modifica el Modelo (eso lo hace el Controlador).
export function useObservar(modelo) {
  const [, redibujar] = useReducer((version) => version + 1, 0)
  useEffect(() => modelo.suscribir(redibujar), [modelo])
}
