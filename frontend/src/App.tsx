
import './styles/config.css'
import './styles/file.css'
import './styles/styles.css'
import './styles/folder.css'

import {TokenProvider}  from "./components/tokenContext"; 
import LoginForm from './components/login/login'
import HandleWindow from './components/handleWindow'


function App() {
  return (
    <div>
    <TokenProvider>
      <HandleWindow/>
      <LoginForm/>
  	</TokenProvider>
    </div>
  )
}

export default App
