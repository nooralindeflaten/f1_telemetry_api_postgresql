import React from "react";
import { Link } from "react-router-dom";

function HomePage() {
  return (
    <div className="home-container">
      <h1>🏁 Welcome to F1 Telemetry!</h1>
      <p>Explore detailed statistics, race results, and driver performances.</p>

      {/* Navigation Links */}
      <div className="nav-buttons">
        <Link to="/drivers" className="btn">🏎️ View Drivers</Link>
        <Link to="/races" className="btn">🏆 View Races</Link>
        <Link to="/results" className="btn">📊 View Results</Link>
      </div>

      {/* Featured Driver Section */}
      <div className="featured-driver">
        <h2>🔥 Featured Driver</h2>
        <p>Check out the latest stats of **Max Verstappen**!</p>
        <Link to="/drivers/33" className="btn">View Profile</Link>
      </div>
    </div>
  );
}

export default HomePage;
