import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Chart } from 'react-google-charts';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

export default function YearPage() {
  const { year } = useParams();
  const [extraData, setExtraData] = useState([]);
  const [economyData, setEconomyData] = useState([]);
  const [mvwData, setMvwData] = useState([]);

  useEffect(() => {
    fetch(`/api/extra-runs/${year}/`).then(r => r.json()).then(d => {
      const rows = [['Team', 'Extra Runs'], ...d.data.map(i => [i.team, i.extra_runs])];
      setExtraData(rows);
    });
    fetch(`/api/top-economy/${year}/`).then(r => r.json()).then(d => {
      const rows = [['Bowler', 'Economy'], ...d.data.map(i => [i.bowler, i.economy])];
      setEconomyData(rows);
    });
    fetch(`/api/matches-vs-wins/${year}/`).then(r => r.json()).then(d => {
      const rows = [['Team', 'Played', 'Won'], ...d.data.map(i => [i.team, i.played, i.won])];
      setMvwData(rows);
    });
  }, [year]);

  return (
    <Container style={{ marginTop: 20 }}>
      <h2>Year: {year}</h2>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <h4>Extra runs conceded per team</h4>
            {extraData.length > 0 && <Chart chartType='PieChart' data={extraData} width='100%' height='300px' />}
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <h4>Top Economical Bowlers</h4>
            {economyData.length > 0 && <Chart chartType='ColumnChart' data={economyData} width='100%' height='300px' />}
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper style={{ padding: 16 }}>
            <h4>Matches played vs won</h4>
            {mvwData.length > 0 && <Chart chartType='BarChart' data={mvwData} width='100%' height='400px' />}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}
