import { Component } from '@angular/core';
import { SidebarComponent } from '../components/sidebar/sidebar';

interface NuitResultat {
  numero: number;
  spo2: string;
  debitNasal: string;
  ronflements: string;
}

@Component({
  selector: 'app-resultats-nuit',
  standalone: true,
  imports: [SidebarComponent],
  templateUrl: './resultats-nuit.html',
  styleUrl: './resultats-nuit.css',
})
export class ResultatsNuit {
  protected readonly nuits: NuitResultat[] = [1, 2, 3]
    .sort((a, b) => a - b)
    .map((numero) => ({
      numero,
      spo2: `/courbe_spo2_nuit_${numero}.png`,
      debitNasal: `/courbe_debit_nasal_nuit_${numero}.png`,
      ronflements: `/ronflements${numero}_vs_temps.png`,
    }));
}
