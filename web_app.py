<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NHL Injury Feed</title>
    <meta http-equiv="refresh" content="3600"> <!-- Auto-refresh every hour -->
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1600px;
            margin: 0 auto;
            padding: 15px;
            background-color: #f5f5f5;
            color: #333;
        }

        .header {
            text-align: center;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            margin: 0;
            font-size: 2em;
            font-weight: 700;
        }

        .stats {
            display: flex;
            justify-content: space-around;
            margin: 15px 0;
            flex-wrap: wrap;
        }

        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            min-width: 120px;
            margin: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .stat-number {
            font-size: 1.5em;
            font-weight: bold;
            color: #d32f2f;
        }

        .stat-number.possible {
            color: #f57c00;
        }

        .stat-label {
            color: #666;
            margin-top: 3px;
            font-size: 0.9em;
        }

        .last-updated {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
            font-size: 0.9em;
        }

        .refresh-info {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 6px;
            padding: 10px;
            margin: 15px 0;
            text-align: center;
            font-size: 0.9em;
        }

        .manual-refresh {
            background: #1976d2;
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
            font-size: 0.85em;
        }

        .manual-refresh:hover {
            background: #1565c0;
        }

        .legend {
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 10px;
            margin: 15px 0;
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 0.85em;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        /* Ultra Compact Team Grid - All teams visible */
        .team-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 8px;
            padding: 0 5px;
        }

        .team-card {
            background: white;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 8px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
            height: 220px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            font-size: 0.85em;
        }

        .team-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
            border-color: #1976d2;
        }

        .team-info {
            text-align: center;
            margin-bottom: 6px;
            padding-bottom: 6px;
            border-bottom: 1px solid #f0f0f0;
            flex-shrink: 0;
        }

        .team-logo {
            font-size: 1.2em;
            font-weight: bold;
            display: block;
            margin-bottom: 2px;
            color: #1976d2;
        }

        .team-code {
            font-size: 0.9em;
            font-weight: bold;
            color: #1976d2;
            margin-bottom: 1px;
        }

        .team-name {
            font-size: 0.7em;
            color: #666;
            margin-bottom: 2px;
        }

        .injury-counts {
            font-size: 0.65em;
            color: #666;
        }

        .confirmed-count {
            color: #d32f2f;
            font-weight: 500;
        }

        .possible-count {
            color: #f57c00;
            font-weight: 500;
        }

        .team-injuries {
            flex-grow: 1;
            overflow-y: auto;
        }

        .injury-entry {
            margin-bottom: 6px;
            padding: 6px 8px;
            background: #f8f9fa;
            border-radius: 4px;
            font-size: 0.75em;
            display: flex;
            align-items: flex-start;
            gap: 6px;
        }

        .injury-entry:last-child {
            margin-bottom: 0;
        }

        .injury-entry.confirmed {
            border-left: 3px solid #d32f2f;
        }

        .injury-entry.possible {
            border-left: 3px solid #f57c00;
            background: #fff8e1;
        }

        .injury-icon {
            font-size: 0.9em;
            margin-top: 1px;
            flex-shrink: 0;
        }

        .injury-icon.confirmed {
            color: #d32f2f;
        }

        .injury-icon.possible {
            color: #f57c00;
        }

        .injury-details {
            flex-grow: 1;
            min-width: 0;
        }

        .injury-entry .player-name {
            font-weight: 600;
            color: #1976d2;
            margin-bottom: 2px;
            line-height: 1.2;
        }

        .injury-entry .injury-type {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 2px;
            line-height: 1.2;
        }

        .injury-entry.confirmed .injury-type {
            color: #d32f2f;
        }

        .injury-entry.possible .injury-type {
            color: #f57c00;
        }

        .return-timeline {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: 500;
            margin-bottom: 2px;
            display: inline-block;
        }

        .return-timeline.day-to-day {
            background: #e3f2fd;
            color: #1976d2;
        }

        .return-timeline.weeks {
            background: #fff3e0;
            color: #f57c00;
        }

        .return-timeline.long-term {
            background: #ffebee;
            color: #d32f2f;
        }

        .return-timeline.season-ending {
            background: #f3e5f5;
            color: #7b1fa2;
        }

        .injury-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.7em;
            color: #666;
            margin-top: 2px;
        }

        .injury-date {
            font-style: italic;
        }

        .injury-source {
            font-weight: 500;
        }

        .confidence {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 1px 4px;
            border-radius: 2px;
            font-size: 0.7em;
            font-weight: 500;
        }

        .no-team-injuries {
            text-align: center;
            padding: 15px 5px;
            color: #4caf50;
            font-style: italic;
            font-size: 0.8em;
        }

        .no-injuries {
            text-align: center;
            padding: 30px;
            color: #4caf50;
            font-size: 1.1em;
        }

        .source-info {
            text-align: center;
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 6px;
            color: #666;
            font-size: 0.85em;
        }

        @media (max-width: 1200px) {
            .team-grid {
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            }

            .team-card {
                height: 200px;
                font-size: 0.8em;
            }
        }

        @media (max-width: 768px) {
            .stats {
                flex-direction: column;
            }

            .legend {
                flex-direction: column;
                gap: 10px;
            }

            .team-grid {
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 6px;
            }

            .team-card {
                height: 180px;
                font-size: 0.75em;
            }
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏒 NHL Injury Feed</h1>
        <p>Confirmed injuries + Possible injury detection • Chronological order</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{{ data.total_count }}</div>
            <div class="stat-label">Confirmed Injuries</div>
        </div>
        <div class="stat-card">
            <div class="stat-number possible">{{ data.possible_count or 0 }}</div>
            <div class="stat-label">Possible Injuries</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{{ data.by_team|length }}</div>
            <div class="stat-label">Teams Affected</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">32</div>
            <div class="stat-label">Teams Visible</div>
        </div>
    </div>

    <div class="legend">
        <div class="legend-item">
            <span style="color: #d32f2f; font-weight: bold;">🏥</span>
            <span>Confirmed Injury (Official Report)</span>
        </div>
        <div class="legend-item">
            <span style="color: #f57c00; font-weight: bold;">⚠️</span>
            <span>Possible Injury (Low Ice Time)</span>
        </div>
    </div>

    {% if data.last_updated %}
    <div class="last-updated">
        📅 Last Updated: {{ data.formatted_time }} • Most recent injuries shown first
    </div>
    {% endif %}

    <div class="refresh-info">
        🔄 Auto-refresh every hour
        <a href="/api/refresh" class="manual-refresh">Manual Refresh</a>
        <a href="/api/injuries" class="manual-refresh">JSON Data</a>
    </div>

    {% if data.team_grid %}
        <!-- Ultra Compact Team Grid - All Teams Visible -->
        <div class="team-grid">
            {% for team in data.team_grid %}
            <div class="team-card">
                <div class="team-info">
                    <div class="team-logo">{{ team.logo }}</div>
                    <div class="team-name">{{ team.name }}</div>
                    <div class="injury-counts">
                        {% if team.injury_count > 0 %}
                        <span class="confirmed-count">{{ team.injury_count }} confirmed</span>
                        {% endif %}
                        {% if team.possible_count > 0 %}
                        {% if team.injury_count > 0 %} | {% endif %}
                        <span class="possible-count">{{ team.possible_count }} possible</span>
                        {% endif %}
                        {% if team.injury_count == 0 and team.possible_count == 0 %}
                        <span style="color: #4caf50;">Healthy</span>
                        {% endif %}
                    </div>
                </div>

                <div class="team-injuries">
                    {% for injury in team.confirmed_injuries %}
                    <div class="injury-entry confirmed">
                        <div class="injury-icon confirmed">🏥</div>
                        <div class="injury-details">
                            <div class="player-name">{{ injury.player }}</div>
                            <div class="injury-type">{{ injury.injury_date or injury.injury_type }}</div>
                            {% if injury.return_timeline %}
                            <div class="return-timeline
                                {% if 'day-to-day' in injury.return_timeline.lower() %}day-to-day
                                {% elif 'week' in injury.return_timeline.lower() %}weeks
                                {% elif 'season' in injury.return_timeline.lower() or 'ltir' in injury.return_timeline.lower() %}season-ending
                                {% elif 'month' in injury.return_timeline.lower() or 'long-term' in injury.return_timeline.lower() %}long-term
                                {% endif %}">
                                {{ injury.return_timeline }}
                            </div>
                            {% endif %}
                            <div class="injury-meta">
                                {% if injury.formatted_date %}
                                <span class="injury-date">{{ injury.formatted_date }}</span>
                                {% endif %}
                                <span class="injury-source">{{ injury.source or 'Official' }}</span>
                            </div>
                        </div>
                    </div>
                    {% endfor %}

                    {% for injury in team.possible_injuries %}
                    <div class="injury-entry possible">
                        <div class="injury-icon possible">⚠️</div>
                        <div class="injury-details">
                            <div class="player-name">{{ injury.player }}</div>
                            <div class="injury-type">{{ injury.reason }}</div>
                            {% if injury.return_timeline %}
                            <div class="return-timeline">{{ injury.return_timeline }}</div>
                            {% endif %}
                            <div class="injury-meta">
                                {% if injury.formatted_date %}
                                <span class="injury-date">{{ injury.formatted_date }}</span>
                                {% endif %}
                                {% if injury.confidence %}
                                <span class="confidence">{{ injury.confidence }}</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}

                    {% if team.injury_count == 0 and team.possible_count == 0 %}
                    <div class="no-team-injuries">
                        ✅ No injuries detected
                    </div>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="no-injuries">
            ✅ No current injuries reported
        </div>
    {% endif %}

    <div class="source-info">
        📊 Confirmed: Hockey-Reference.com | Possible: NHL Stats API (Ice Time Analysis)
        <br>
        🔄 Updates every hour automatically • Injuries sorted by date (newest first)
        <br>
        💻 <a href="https://github.com/jakehari/nhl-injury-feed" style="color: #1976d2;">View Source Code</a>
    </div>

    <script>
        // Add loading state for manual refresh
        document.addEventListener('DOMContentLoaded', function() {
            const refreshLinks = document.querySelectorAll('a[href="/api/refresh"]');
            refreshLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    this.textContent = 'Refreshing...';
                    fetch('/api/refresh')
                        .then(() => {
                            window.location.reload();
                        })
                        .catch(() => {
                            this.textContent = 'Refresh Failed';
                            setTimeout(() => {
                                this.textContent = 'Manual Refresh';
                            }, 2000);
                        });
                });
            });
        });
    </script>
</body>
</html>