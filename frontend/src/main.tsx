import React from 'react';
import { createRoot } from 'react-dom/client';
import 'maplibre-gl/dist/maplibre-gl.css';
import './styles.css';
import StaticApp from './ui/StaticApp';
createRoot(document.getElementById('root')!).render(<React.StrictMode><StaticApp /></React.StrictMode>);
