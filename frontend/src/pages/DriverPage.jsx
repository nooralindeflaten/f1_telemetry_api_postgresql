import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function DriverPage() {
  const { driverId } = useParams();
  const [driver, setDriver] = useState(null);
  const [results, setResults] = useState([]);
  const [races, setRaces] = useState([]);
  const [qualifying, setQualifying] = useState([]);
  const [standings, setStandings] = useState([]);
  const [sprintResults, setSprintResults] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [seasonData, setSeasonData] = useState({});
  const [filteredSeason, setFilteredSeason] = useState(null);
  const [selectedRace, setSelectedRace] = useState(null);
  const [pitStops, setPitStops] = useState([]);
  const [lapTimes, setLapTimes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    Promise.all([
      fetch(`http://127.0.0.1:8000/drivers/${driverId}`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/drivers/${driverId}/results`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/drivers/${driverId}/races`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/drivers/${driverId}/qualifying`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/drivers/${driverId}/driver_standings`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/drivers/${driverId}/sprint_results`).then((res) => res.json()),
      fetch(`http://127.0.0.1:8000/seasons/`).then((res) => res.json()),
    ])
      .then(([driverData, resultsData, racesData, qualifyingData, standingsData, sprintResultsData, seasonsData]) => {
        setDriver(driverData);
        setResults(resultsData);
        setRaces(racesData);
        setQualifying(qualifyingData);
        setStandings(standingsData);
        setSprintResults(sprintResultsData);

        // Create a map for { seasonId: year }
        const seasonMap = seasonsData.reduce((acc, season) => {
          acc[season.seasonId] = season.year;
          return acc;
        }, {});
        setSeasonData(seasonMap);

        // Extract unique seasons from races
        const uniqueSeasons = [...new Set(racesData.map((r) => r.seasonId))];
        setSeasons(uniqueSeasons);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setError("Failed to load data.");
      })
      .finally(() => setLoading(false));
  }, [driverId]);

  const handleRaceClick = async (raceId) => {
    setSelectedRace(raceId);
    setPitStops([]);
    setLapTimes([]);

    try {
      const response = await fetch(`http://127.0.0.1:8000/drivers/${driverId}/races/${raceId}/full_data/`);
      const data = await response.json();

      if (data.error) {
        console.error("Error:", data.error);
        return;
      }

      setPitStops(data.pit_stops || []);
      setLapTimes(data.lap_times || []);
      setResults(data.result ? [data.result] : []);
    } catch (error) {
      console.error("Error fetching combined driver race data:", error);
    }
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Driver {driverId} Details</h1>

      {/* DRIVER SUMMARY */}
      {driver && (
        <div className="mt-4 p-4 border rounded-md shadow">
          <h2 className="text-xl font-bold">{driver.forename} {driver.surname}</h2>
          <p><strong>Nationality:</strong> {driver.nationality}</p>
          <p><strong>Date of Birth:</strong> {driver.dob}</p>
          <p><strong>Total Points:</strong> {standings.reduce((acc, s) => acc + s.points, 0)}</p>
        </div>
      )}

      {/* SEASON FILTER */}
      <div className="mt-4">
        <label className="mr-2">Filter by Season:</label>
        <select onChange={(e) => setFilteredSeason(Number(e.target.value))} className="border p-2 rounded-md">
          <option value="">All Seasons</option>
          {seasons.map((seasonId) => (
            <option key={seasonId} value={seasonId}>
              {seasonData[seasonId] || seasonId}
            </option>
          ))}
        </select>
      </div>

      {/* RACES PARTICIPATION */}
      <div className="mt-4">
        <h2 className="text-xl font-bold">Races</h2>
        <ul>
          {races
            .filter((r) => !filteredSeason || r.seasonId === filteredSeason)
            .map((r) => (
              <li key={r.raceId} className="cursor-pointer text-blue-500 hover:underline" onClick={() => handleRaceClick(r.raceId)}>
                {r.name} ({seasonData[r.seasonId] || r.seasonId})
              </li>
            ))}
        </ul>
      </div>

      {/* RESULTS TABLE */}
      <div className="mt-4">
        <h2 className="text-xl font-bold">Race Results</h2>
        <table className="w-full border-collapse border">
          <thead>
            <tr className="bg-gray-200">
              <th className="border p-2">Result ID</th>
              <th className="border p-2">Points</th>
              <th className="border p-2">Fastest Lap Speed</th>
              <th className="border p-2">Season</th>
            </tr>
          </thead>
          <tbody>
            {results
              .filter((r) => !filteredSeason || r.seasonId === filteredSeason)
              .map((r) => (
                <tr key={r.raceId} className="border">
                  <td className="border p-2">{r.resultId || r.resultId}</td>
                  <td className="border p-2">{r.points}</td>
                  <td className="border p-2">{r.fastestLapSpeed || "N/A"}</td>
                  <td className="border p-2">{seasonData[r.seasonId] || r.seasonId}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      {/* EXTRA DATA (Pit Stops & Lap Times) */}
      {selectedRace && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">Race Details for {selectedRace}</h2>

          {/* Pit Stops */}
          <h3 className="text-lg font-bold mt-2">Pit Stops</h3>
          {pitStops.length > 0 ? (
            <ul>
              {pitStops.map((p, index) => (
                <li key={index}>{p.lap}: {p.time}</li>
              ))}
            </ul>
          ) : <p>No pit stop data available.</p>}

          {/* Lap Times */}
          <h3 className="text-lg font-bold mt-2">Lap Times</h3>
          {lapTimes.length > 0 ? (
            <ul>
              {lapTimes.map((l, index) => (
                <li key={index}>{l.lap}: {l.time}</li>
              ))}
            </ul>
          ) : <p>No lap time data available.</p>}
        </div>
      )}
    </div>
  );
}

export default DriverPage;