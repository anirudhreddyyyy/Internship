<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Analysis Report - test.md</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { opacity: 0.9; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-icon { font-size: 3em; margin-bottom: 10px; }
        .stat-value { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .chart-container {
            position: relative;
            height: 300px;
            margin: 20px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        tr:hover { background: #f5f5f5; }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-success { background: #d4edda; color: #155724; }
        .badge-danger { background: #f8d7da; color: #721c24; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Markdown Analysis Report</h1>
            <p>test.md</p>
            <p style="font-size: 0.9em; opacity: 0.8;">Generated on 2026-01-23 11:18:27</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-value">1,494</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📑</div>
                <div class="stat-value">22</div>
                <div class="stat-label">Headings</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🔗</div>
                <div class="stat-value">43</div>
                <div class="stat-label">Links</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🖼️</div>
                <div class="stat-value">1</div>
                <div class="stat-label">Images</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📑 Heading Distribution</h2>
                <div class="chart-container">
                    <canvas id="headingChart"></canvas>
                </div>
            </div>
            
            <div class="section">
                <h2>🔗 Link Analysis</h2>
                <div class="chart-container" style="height: 200px;">
                    <canvas id="linkChart"></canvas>
                </div>
                
                <h3 style="margin-top: 30px; color: #dc3545;">⚠️ Broken Links (2)</h3>
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>https://ragflow.io/docs/dev/release_notes</td><td><span class='badge badge-danger'>Broken (404)</span></td></tr><tr><td>https://twitter.com/infiniflowai</td><td><span class='badge badge-danger'>Broken (403)</span></td></tr>
                    </tbody>
                </table>
                
            </div>
            
            
            <div class="section">
                <h2>🖼️ Images</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Alt Text</th>
                            <th>URL</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><em>(no alt text)</em></td><td>https://github.com/user-attachments/assets/0daf462c-a24d-4496-a66f-92533534e187</td></tr>
                    </tbody>
                </table>
            </div>
            
        </div>
        
        <div class="footer">
            <p>Generated by Markdown File Analyzer</p>
        </div>
    </div>
    
    <script>
        // Heading Distribution Chart
        const headingCtx = document.getElementById('headingChart').getContext('2d');
        new Chart(headingCtx, {
            type: 'bar',
            data: {
                labels: ['H2', 'H3'],
                datasets: [{
                    label: 'Count',
                    data: [14, 8],
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
        
        // Link Status Chart
        const linkCtx = document.getElementById('linkChart').getContext('2d');
        new Chart(linkCtx, {
            type: 'doughnut',
            data: {
                labels: ['Valid Links', 'Broken Links'],
                datasets: [{
                    data: [41, 2],
                    backgroundColor: ['rgba(40, 167, 69, 0.6)', 'rgba(220, 53, 69, 0.6)'],
                    borderColor: ['rgba(40, 167, 69, 1)', 'rgba(220, 53, 69, 1)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    </script>
</body>
</html>
