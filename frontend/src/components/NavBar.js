import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';

export default function NavBar() {
  return (
    <AppBar position='static'>
      <Toolbar>
        <Typography variant='h6' style={{ flexGrow: 1 }}>IPL Dashboard</Typography>
        <Button color='inherit' component={Link} to='/'>Home</Button>
        <Button color='inherit' component={Link} to='/year/2017'>Year View</Button>
      </Toolbar>
    </AppBar>
  );
}
