import { useState } from "react";
import axios from "axios";

const DriverSearch = () => {
  const [driver_id, setDriverId] = useState("");
  const [driver, setDriver] = useState(null);
  const [error, setError] = useState(null);

  const fetchDriver = async () => {
    console.log("Fetch Driver")
    if (!driver_id.trim()) {
      setError("Please enter a driver ID.");
      setDriver(null);
      return;
    }

    try {
      setError(null);
      const response = await axios.get(`http://127.0.0.1:8000/drivers/${parseInt(driver_id, 10)}`);
      console.log(response.data);
      setDriver(response.data);
    } catch (err) {
      setError("Driver not found!");
      setDriver(null);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Search for a Driver</h2>
      <input
        type="number"
        value={driver_id}
        onChange={(e) => setDriverId(e.target.value)}
        placeholder="Enter driver ID (e.g., 1)"
        className="border p-2 rounded-md"
      />
      <button onClick={fetchDriver} className="bg-blue-500 text-white p-2 ml-2 rounded-md">
        Search
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}

      {driver && (
        <div className="mt-4 p-4 border rounded-md">
          <h3 className="text-lg font-bold">{driver.forename} {driver.surname}</h3>
          <p><strong>Nationality:</strong> {driver.nationality}</p>
          <p><strong>DOB:</strong> {driver.dob}</p>
          <p><strong>Number:</strong> {driver.number || "N/A"}</p>
          <p><strong>Code:</strong> {driver.code || "N/A"}</p>
        </div>
      )}
    </div>
  );
};

export default DriverSearch;

