import { useEffect, useState } from 'react'
import { Estado } from '../modelos/ModeloBusqueda.js'
import {
  formatearDuracion,
  formatearEvalue,
  formatearHora,
  formatearPorcentaje,
  formatearScore,
} from './formato.js'
import { useObservar } from './useObservar.js'

// PantallaBusqueda (Vista, «boundary»).
// - Delega la única acción del investigador ("Ejecutar búsqueda") en ControladorBusqueda.
// - Observa a ModeloBusqueda y ModeloResultados para leer qué dibujar (DA-07).
// - No contiene reglas del negocio ni habla con el Backend.
export function PantallaBusqueda({ controlador, modeloBusqueda, modeloResultados, ejemplos }) {
  useObservar(modeloBusqueda)
  useObservar(modeloResultados)
  // Sección visible: es solo navegación de la interfaz. Cambiarla no interrumpe la ejecución,
  // porque el estado de la búsqueda vive en los Modelos y no en esta pantalla (CA-01).
  const [seccion, setSeccion] = useState('busqueda')

  const estado = modeloBusqueda.estado()

  return (
    <>
      <header className="barra-superior">
        <span className="marca">
          LocalBlast <small>· GUI para BLAST+</small>
        </span>
      </header>
      <div className="disposicion">
        <nav className="lateral" aria-label="Secciones">
          <div className="titulo-seccion">Trabajo actual</div>
          <button
            className={seccion === 'busqueda' ? 'enlace activo' : 'enlace'}
            onClick={() => setSeccion('busqueda')}
          >
            Búsqueda actual
            <ChipEstado estado={estado} />
          </button>
          <div className="titulo-seccion">Ayuda</div>
          <button
            className={seccion === 'ayuda' ? 'enlace activo' : 'enlace'}
            onClick={() => setSeccion('ayuda')}
          >
            Cómo leer los resultados
          </button>
        </nav>
        <main className="principal">
          <AvisoAccesible estado={estado} cantidad={modeloResultados.filas().length} />
          {seccion === 'busqueda' ? (
            <SeccionBusqueda
              controlador={controlador}
              modeloBusqueda={modeloBusqueda}
              modeloResultados={modeloResultados}
            />
          ) : (
            <SeccionAyuda ejemplos={ejemplos} estado={estado} />
          )}
        </main>
      </div>
    </>
  )
}

function SeccionBusqueda({ controlador, modeloBusqueda, modeloResultados }) {
  const estado = modeloBusqueda.estado()
  const configuracion = modeloBusqueda.configuracion()
  const ejecutar = () => controlador.ejecutar()

  return (
    <div className="contenedor">
      <Pasos estado={estado} />
      {estado === Estado.VALIDADA && mostrar_busqueda_validada(configuracion, ejecutar)}
      {estado === Estado.EN_EJECUCION && <Progreso modeloBusqueda={modeloBusqueda} />}
      {estado === Estado.CON_ERROR &&
        mostrar_error(modeloBusqueda.mensaje_error(), configuracion, ejecutar)}
      {estado === Estado.FINALIZADA &&
        mostrar_resultados(modeloResultados.filas(), configuracion, modeloBusqueda)}
    </div>
  )
}

// --- Estados que dibuja la pantalla (nombres de las secuencias) --------------------

function mostrar_busqueda_validada(configuracion, ejecutar) {
  return (
    <>
      <h1 className="titulo-pagina">Ejecutar la búsqueda</h1>
      <p className="subtitulo-pagina">
        La configuración ya está validada. Al ejecutarla, BLAST+ corre en segundo plano y la
        búsqueda se guarda automáticamente en el historial cuando termina.
      </p>
      <section className="panel">
        <div className="cabecera-panel">
          <h2>Búsqueda lista para ejecutar</h2>
          <span className="chip chip-exito">✓ Configuración validada</span>
        </div>
        <ResumenConfiguracion configuracion={configuracion} />
        <details className="query">
          <summary>Ver la secuencia query</summary>
          <pre>{configuracion.secuencia}</pre>
        </details>
        <div className="fila-botones">
          <button className="boton boton-primario" onClick={ejecutar}>
            Ejecutar búsqueda
          </button>
        </div>
      </section>
    </>
  )
}

function Progreso({ modeloBusqueda }) {
  const configuracion = modeloBusqueda.configuracion()
  const transcurrido = useTiempoTranscurrido(modeloBusqueda.inicio())
  return mostrar_progreso(configuracion, modeloBusqueda.inicio(), transcurrido)
}

function mostrar_progreso(configuracion, inicio, transcurrido) {
  return (
    <>
      <h1 className="titulo-pagina">Ejecución de la búsqueda</h1>
      <p className="subtitulo-pagina">
        BLAST+ está procesando tu consulta en segundo plano. Podés navegar por el resto de la
        aplicación mientras tanto; esta ejecución no se interrumpe.
      </p>
      <section className="panel" aria-busy="true">
        <div className="cabecera-progreso">
          <div className="girador" aria-hidden="true" />
          <div>
            <h2>
              Ejecutando <code>{configuracion.variante}</code> contra{' '}
              <span>{configuracion.base_datos_nombre ?? configuracion.base_datos}</span> (
              {configuracion.modo === 'remoto' ? 'NCBI remoto' : 'local'})
            </h2>
            <p>Vas a ver los resultados en esta misma pantalla cuando BLAST+ termine.</p>
          </div>
        </div>
        <div className="barra-progreso" role="progressbar" aria-label="Ejecución en curso">
          <div className="relleno-indeterminado" />
        </div>
        <div className="meta-progreso">
          <span>
            BLAST+ no informa su avance: el tiempo depende del tamaño de la base.
            <span className="chip chip-aviso">⚠ aún no guardada en el historial</span>
          </span>
          <span>
            Tiempo transcurrido: <b>{formatearDuracion(transcurrido)}</b>
          </span>
        </div>
        <ResumenConfiguracion configuracion={configuracion} inicio={inicio} />
        <div className="caja-ayuda">
          <strong>Podés seguir trabajando.</strong> La búsqueda sigue corriendo aunque cambies
          de sección; en la barra lateral vas a ver su estado. Se guarda automáticamente en el
          historial al finalizar.
        </div>
      </section>
    </>
  )
}

function mostrar_error(mensaje, configuracion, reintentar) {
  return (
    <>
      <h1 className="titulo-pagina">Ejecución de la búsqueda</h1>
      <section className="panel">
        <div className="aviso aviso-error" role="alert">
          <span className="icono">⚠</span>
          <div>
            <strong>La búsqueda no se pudo completar.</strong>
            <br />
            No se muestra ninguna tabla y la búsqueda <em>no</em> quedó guardada en el historial.
            Este es el mensaje recibido, tal cual lo informó el sistema:
          </div>
        </div>
        <pre className="error-literal">
          <span className="etiqueta">[mensaje recibido]</span>
          {'\n'}
          {mensaje}
        </pre>
        <ResumenConfiguracion configuracion={configuracion} />
        <div className="fila-botones">
          <button className="boton boton-primario" onClick={reintentar}>
            Reintentar búsqueda
          </button>
        </div>
      </section>
    </>
  )
}

function mostrar_resultados(filas, configuracion, modeloBusqueda) {
  return (
    <>
      <div className="cabecera-resultados">
        <div>
          <h1 className="titulo-pagina">Resultados de la búsqueda</h1>
          <p className="subtitulo-pagina">
            {filas.length === 1
              ? '1 alineamiento encontrado.'
              : `${filas.length} alineamientos encontrados.`}{' '}
            Se muestran todos los que devolvió BLAST+, ordenados por E-value.
          </p>
        </div>
        <span className="chip chip-exito chip-grande">
          ✓ Guardado en el historial · {formatearHora(modeloBusqueda.fin())}
        </span>
      </div>
      <BarraResumen configuracion={configuracion} inicio={modeloBusqueda.inicio()} />
      <section className="panel panel-tabla">
        {filas.length === 0 ? (
          <div className="sin-hits">
            <strong>BLAST+ terminó sin alineamientos</strong> por debajo del E-value máximo
            configurado. La búsqueda igual quedó guardada en el historial.
          </div>
        ) : (
          <TablaResultados filas={filas} />
        )}
      </section>
    </>
  )
}

// --- Piezas de la pantalla ------------------------------------------------------------

const COLUMNAS = [
  {
    titulo: 'Hit ID',
    ayuda: 'Identificador de la secuencia de la base que se alineó con tu query.',
  },
  { titulo: 'Descripción', ayuda: null },
  {
    titulo: 'Score',
    ayuda: 'Bit score del mejor alineamiento con ese hit. Más alto = alineamiento más fuerte.',
    numerica: true,
  },
  {
    titulo: 'E-value obs.',
    ayuda:
      'E-value observado: cuántos alineamientos con este score se esperarían por azar en una base de este tamaño. Más bajo = más significativo.',
    numerica: true,
  },
  {
    titulo: '% identidad',
    ayuda: 'Porcentaje de posiciones idénticas dentro del alineamiento.',
    numerica: true,
  },
  {
    titulo: '% cobertura',
    ayuda: 'Porcentaje de la query que cubre el alineamiento.',
    numerica: true,
  },
]

function TablaResultados({ filas }) {
  return (
    <div className="envoltorio-tabla">
      <table className="tabla">
        <thead>
          <tr>
            {COLUMNAS.map((columna) => (
              <th key={columna.titulo} className={columna.numerica ? 'numerica' : undefined}>
                {columna.titulo}
                {columna.ayuda && <Ayuda texto={columna.ayuda} />}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {filas.map((fila, indice) => (
            <tr key={`${fila.id_hit}-${indice}`}>
              <td className="mono">{fila.id_hit}</td>
              <td className="descripcion">{fila.descripcion}</td>
              <td className="numerica mono">{formatearScore(fila.score)}</td>
              <td className="numerica mono">{formatearEvalue(fila.evalue)}</td>
              <td className="numerica">
                <Porcentaje valor={fila.porcentaje_identidad} />
              </td>
              <td className="numerica">
                <Porcentaje valor={fila.porcentaje_cobertura} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Porcentaje({ valor }) {
  return (
    <span className="porcentaje">
      <span className="mono">{formatearPorcentaje(valor)}</span>
      <span className="minibarra" aria-hidden="true">
        <span style={{ width: `${Math.min(valor, 100)}%` }} />
      </span>
    </span>
  )
}

function Ayuda({ texto }) {
  return (
    <span className="ayuda" tabIndex={0} aria-label={texto}>
      ?<span className="globo" role="tooltip">{texto}</span>
    </span>
  )
}

function ResumenConfiguracion({ configuracion, inicio }) {
  const parametros = configuracion.parametros ?? {}
  const datos = [
    ['Modo', configuracion.modo === 'remoto' ? 'Remoto (NCBI)' : 'Local'],
    ['Variante BLAST', <code key="v">{configuracion.variante}</code>],
    ['Base de datos', configuracion.base_datos_nombre ?? configuracion.base_datos],
    ['E-value máximo', parametros.evalue ?? '—'],
    ['Query', describirQuery(configuracion)],
    ['Matriz', parametros.matrix ?? '—'],
    ['Tamaño de palabra', parametros.word_size ?? '—'],
    ['Gaps (apertura / extensión)', `${parametros.gapopen ?? '—'} / ${parametros.gapextend ?? '—'}`],
  ]
  if (inicio) datos.push(['Iniciada', formatearHora(inicio)])
  return (
    <dl className="resumen">
      {datos.map(([nombre, valor]) => (
        <div key={nombre}>
          <dt>{nombre}</dt>
          <dd>{valor}</dd>
        </div>
      ))}
    </dl>
  )
}

function BarraResumen({ configuracion, inicio }) {
  const parametros = configuracion.parametros ?? {}
  return (
    <div className="barra-resumen">
      <span>
        <b>Query:</b> {describirQuery(configuracion)}
      </span>
      <span>
        <b>Variante:</b> <code>{configuracion.variante}</code>
      </span>
      <span>
        <b>Base:</b> {configuracion.base_datos_nombre ?? configuracion.base_datos} (
        {configuracion.modo === 'remoto' ? 'NCBI remoto' : 'local'})
      </span>
      <span>
        <b>E-value máx:</b> {parametros.evalue ?? '—'}
      </span>
      <span>
        <b>Iniciada:</b> {formatearHora(inicio)}
      </span>
    </div>
  )
}

function describirQuery(configuracion) {
  const partes = [configuracion.query_nombre ?? 'query']
  if (configuracion.query_longitud) {
    partes.push(`${configuracion.query_longitud} ${configuracion.query_unidad ?? ''}`.trim())
  }
  return partes.join(' · ')
}

const PASOS = ['Secuencia query', 'Configuración', 'Ejecución', 'Resultados']

function Pasos({ estado }) {
  const actual = estado === Estado.FINALIZADA ? 3 : 2
  return (
    <ol className="pasos">
      {PASOS.map((paso, indice) => (
        <li
          key={paso}
          className={indice < actual ? 'hecho' : indice === actual ? 'actual' : undefined}
          aria-current={indice === actual ? 'step' : undefined}
        >
          <span className="numero">{indice < actual ? '✓' : indice + 1}</span>
          {paso}
        </li>
      ))}
    </ol>
  )
}

const TEXTO_ESTADO = {
  [Estado.VALIDADA]: { texto: 'lista', clase: 'chip-neutro' },
  [Estado.EN_EJECUCION]: { texto: 'corriendo', clase: 'chip-corriendo' },
  [Estado.FINALIZADA]: { texto: 'resultados listos', clase: 'chip-exito' },
  [Estado.CON_ERROR]: { texto: 'con error', clase: 'chip-error' },
}

function ChipEstado({ estado }) {
  const { texto, clase } = TEXTO_ESTADO[estado]
  return (
    <span className={`chip chip-lateral ${clase}`}>
      {estado === Estado.EN_EJECUCION && <span className="punto" aria-hidden="true" />}
      {texto}
    </span>
  )
}

// Anuncia los cambios de estado a lectores de pantalla (visibilidad del estado del sistema).
function AvisoAccesible({ estado, cantidad }) {
  const mensajes = {
    [Estado.VALIDADA]: '',
    [Estado.EN_EJECUCION]: 'La búsqueda se está ejecutando.',
    [Estado.FINALIZADA]: `La búsqueda terminó con ${cantidad} alineamientos y quedó guardada en el historial.`,
    [Estado.CON_ERROR]: 'La búsqueda no se pudo completar.',
  }
  return (
    <div className="solo-lectores" aria-live="polite">
      {mensajes[estado]}
    </div>
  )
}

function SeccionAyuda({ ejemplos, estado }) {
  return (
    <div className="contenedor">
      <h1 className="titulo-pagina">Cómo leer los resultados</h1>
      <p className="subtitulo-pagina">
        Qué significa cada columna de la tabla de resultados.
        {estado === Estado.EN_EJECUCION &&
          ' Tu búsqueda sigue corriendo en segundo plano mientras leés esto; su estado se ve en la barra lateral.'}
      </p>
      <section className="panel">
        <dl className="glosario">
          {COLUMNAS.filter((columna) => columna.ayuda).map((columna) => (
            <div key={columna.titulo}>
              <dt>{columna.titulo}</dt>
              <dd>{columna.ayuda}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="panel">
        <h2>Datos de demostración</h2>
        <p className="texto-tenue">
          La carga y la validación de la búsqueda son otras historias de usuario, así que la
          pantalla arranca con una búsqueda ya validada. Estas son las disponibles:
        </p>
        <ul className="lista-ejemplos">
          {Object.entries(ejemplos).map(([clave, ejemplo]) => (
            <li key={clave}>
              <a href={`?ejemplo=${clave}`}>{ejemplo.titulo}</a>
              <span className="texto-tenue"> — {ejemplo.descripcion}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

function useTiempoTranscurrido(inicio) {
  const [ahora, setAhora] = useState(() => Date.now())
  useEffect(() => {
    const intervalo = setInterval(() => setAhora(Date.now()), 1000)
    return () => clearInterval(intervalo)
  }, [])
  return inicio ? ahora - inicio.getTime() : 0
}
