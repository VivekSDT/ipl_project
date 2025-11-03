import React, { useEffect, useState } from 'react';
import { Chart } from 'react-google-charts';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

export default function Landing() {
  const [matchesData, setMatchesData] = useState([]);
  const [winsData, setWinsData] = useState([]);

  useEffect(() => {
    fetch('/api/matches-per-year/').then(r => r.json()).then(d => {
      const rows = [['Season', 'Matches'], ...d.data.map(i => [String(i.season), i.matches])];
      setMatchesData(rows);
    });
    fetch('/api/stacked-wins/').then(r => r.json()).then(d => {
      const bySeason = {};
      const teams = new Set();
      d.data.forEach(item => {
        teams.add(item.team);
        bySeason[item.season] = bySeason[item.season] || {};
        bySeason[item.season][item.team] = item.wins;
      });
      const teamList = Array.from(teams).sort();
      const header = ['Season', ...teamList];
      const rows = [header];
      Object.keys(bySeason).sort().forEach(season => {
        const row = [String(season)];
        teamList.forEach(t => row.push(bySeason[season][t] || 0));
        rows.push(row);
      });
      setWinsData(rows);
    });
  }, []);

  return (
    <Container style={{ marginTop: 20 }}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <h3>Matches per Year</h3>
            {matchesData.length > 0 && (
              <Chart chartType='ColumnChart' data={matchesData} width='100%' height='300px' options={{legend: {position: 'none'}}} />
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <h3>Matches Won per Team (stacked)</h3>
            {winsData.length > 0 && (
              <Chart chartType='BarChart' data={winsData} width='100%' height='350px' options={{isStacked: true}} />
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
