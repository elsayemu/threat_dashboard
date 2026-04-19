// Function to fetch threat data from the backend API
async function loadThreats() {
    // Send request to backend
    const res = await fetch('/api/threats');

    // Convert response to JSON
    const data = await res.json();

    // Get reference to the table body
    const table = document.getElementById('threatTable');

    // Clear existing table content before inserting data
    table.innerHTML = "";

    // Loop for each record
    data.forEach(t => {

        // Determines color based on threat score
        let color = t.score > 80 ? "red" : (t.score > 50 ? "orange" : "green");

        // Create a table row
        const row = `
            <tr>
                <td>${t.ip}</td>
                <td style="color:${color}">${t.score}</td>
                <td>${t.country}</td>
                <td>${t.timestamp}</td>
            </tr>
        `;

        // Append the row to the table
        table.innerHTML += row;
    });
}

// Data loads when page first opens
loadThreats();

// Automatically refresh data every 10 seconds (10000 ms)
setInterval(loadThreats, 10000);