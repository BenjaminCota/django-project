import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import 'semantic-ui-css/semantic.min.css'
import 'react-toastify/dist/ReactToastify.css'

// Nota: semantic-ui-react usa findDOMNode internamente, lo cual genera
// warnings bajo StrictMode; por eso no se envuelve la app en <StrictMode>.
createRoot(document.getElementById('root')).render(<App />)
