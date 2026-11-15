import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { demoRecords } from '../data/demo';
import DataExplorer from './DataExplorer';

afterEach(cleanup);

describe('DataExplorer', () => {
  it('searches selected records and shows an informative empty result', () => {
    render(<DataExplorer records={demoRecords}/>);
    expect(screen.getByText(/1–25 of 30 matching records/)).toBeTruthy();
    fireEvent.change(screen.getByLabelText('Search selected records'), { target: { value: 'not a source' } });
    expect(screen.getByText('No records match this search.')).toBeTruthy();
    expect(screen.getByText('0 matching records')).toBeTruthy();
  });

  it('provides an empty state when no dataset is loaded', () => {
    render(<DataExplorer records={[]}/>);
    expect(screen.getByText(/No source records loaded/)).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Export filtered CSV' })).toHaveProperty('disabled', true);
  });
});
