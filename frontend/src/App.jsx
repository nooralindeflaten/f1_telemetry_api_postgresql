import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage";
import DriverPage from "./pages/DriverPage";

function App() {
  return (
    <Router>
      <div className="app">
        {/* Navigation Bar */}
        <nav>
          <ul>
            <li><Link to="/">🏠 Home</Link></li>
            <li><Link to="/drivers/1">🏎️ Driver 1</Link></li>
            <li><Link to="/drivers/2">🏎️ Driver 2</Link></li>
          </ul>
        </nav>

        {/* Page Routing */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/drivers/:driverId" element={<DriverPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

