// Import dependencies
import logo from './logo.svg';
import './App.css';
import LandingPage from './components/LandingPage';
import {Route, BrowserRouter as Router, Routes} from 'react-router-dom'
import ScanPage from './components/ScanPage';
function App() {
  return (
    <Router>
        <Routes>
          <Route path='/' element={<LandingPage />}/>
          <Route path='/scan' exact element={<ScanPage />} />
        </Routes>
    </Router>
  );
}

export default App;
