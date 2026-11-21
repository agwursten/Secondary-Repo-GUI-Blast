// Punto de arranque de la Aplicación Web: el único lugar que crea y conecta las piezas del MVC.
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ejemplos from './busquedas-validadas.json'
import { ClienteBackend } from './cliente/ClienteBackend.js'
import { ControladorBusqueda } from './controladores/ControladorBusqueda.js'
import { ModeloBusqueda } from './modelos/ModeloBusqueda.js'
import { ModeloResultados } from './modelos/ModeloResultados.js'
import { PantallaBusqueda } from './pantallas/PantallaBusqueda.jsx'
import './estilos.css'

// La carga y la validación (HU01 a HU07) no forman parte de esta HU: la pantalla arranca
// con una búsqueda ya validada, elegida con ?ejemplo=<clave> (por defecto, la de demostración).
const clave = new URLSearchParams(window.location.search).get('ejemplo')
const ejemplo = ejemplos[clave] ?? ejemplos.demostracion

const modeloBusqueda = new ModeloBusqueda(ejemplo.configuracion)
const modeloResultados = new ModeloResultados()
const controlador = new ControladorBusqueda(modeloBusqueda, modeloResultados, new ClienteBackend())

createRoot(document.getElementById('raiz')).render(
  <StrictMode>
    <PantallaBusqueda
      controlador={controlador}
      modeloBusqueda={modeloBusqueda}
      modeloResultados={modeloResultados}
      ejemplos={ejemplos}
    />
  </StrictMode>,
)
