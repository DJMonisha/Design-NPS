const data = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October'],
  datasets: [{
      label: 'User Increase',
      data: [65, 59, 80, 81, 56, 55, 40, 75, 60, 70],
      borderColor: '#007bff',
      backgroundColor: 'rgba(0, 123, 255, 0.1)',
      tension: 0.4, 
      fill: true, 
      borderWidth: 2 
  }]
  };


  const config = {
  type: 'line',
  data: data,
  options: {
      responsive: true,
      plugins: {
      legend: {
          position: 'top', 
      },
      tooltip: {
          mode: 'index', 
      }
      },
      scales: {
      x: {
          display: true,
          title: {
          display: true,
          text: 'Month'
          }
      },
      y: {
          display: true,
          title: {
          display: true,
          text: 'Value'
          }
      }
      }
  },
  };


  const ctx = document.getElementById('myLineChart').getContext('2d');


  const myLineChart = new Chart(ctx, config);

          function downloadCSV() {
              const rows = document.querySelectorAll("table tr");
              let csvContent = "data:text/csv;charset=utf-8,";

              rows.forEach(row => {
                  const cols = row.querySelectorAll("td, th");
                  const rowData = Array.from(cols).map(col => col.innerText).join(",");
                  csvContent += rowData + "\r\n";
              });

              const encodedUri = encodeURI(csvContent);
              const link = document.createElement("a");
              link.setAttribute("href", encodedUri);
              link.setAttribute("download", "table_data.csv");
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
          }