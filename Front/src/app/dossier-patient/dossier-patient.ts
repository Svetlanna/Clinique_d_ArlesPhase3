import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth';
import { SidebarComponent } from '../components/sidebar/sidebar';

import { jsPDF } from 'jspdf';
@Component({
  selector: 'app-dossier-patient',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './dossier-patient.html',
  styleUrl: './dossier-patient.css',
})
export class DossierPatient implements OnInit {
  private authService = inject(AuthService);

  // Données exposées par le service
  patients = this.authService.patients;
  resultats = this.authService.resultats;
  patientDetail = this.authService.patientDetail;

  recherche = signal('');
  selectedPatientId = signal<number | null>(null);
  nuitOuverte = signal<number | null>(null);
  chargementResultats = signal(false);

  patientsFiltres = computed(() => {
    const terme = this.recherche().trim().toLowerCase();
    if (!terme) return this.patients();
    return this.patients().filter((p: any) => p.patient?.toLowerCase().includes(terme));
  });

  patientSelectionne = computed(
    () => this.patients().find((p: any) => p.id_patient === this.selectedPatientId()) ?? null,
  );

  ngOnInit() {
    this.authService.fetchPatients().subscribe({
      next: () => console.log('Patients chargés'),
      error: (err: any) => console.error('Erreur API patients:', err),
    });
  }

  onRechercheChange(valeur: string) {
    this.recherche.set(valeur);
  }

  selectionnerPatient(idPatient: number) {
    this.selectedPatientId.set(idPatient);
    this.nuitOuverte.set(null);
    this.chargementResultats.set(true);

    this.authService.fetchPatientDetail(idPatient).subscribe({
      error: (err: any) => console.error('Erreur API détail patient:', err),
    });

    this.authService.fetchResultats(idPatient).subscribe({
      next: () => this.chargementResultats.set(false),
      error: (err: any) => {
        console.error('Erreur API résultats:', err);
        this.chargementResultats.set(false);
      },
    });
  }



  genererFichierPatientPDF() {
  const detail = this.patientDetail();

  // 1. Protection contre les données nulles
  if (!detail || !detail.patient || !detail.dernierSuivi) {
    alert("Données patient indisponibles.");
    return;
  }

  const doc = new jsPDF();
  const p = detail.patient;
  const s = detail.dernierSuivi;

  // 2. Configuration esthétique
  doc.setFont("helvetica", "bold");
  doc.setFontSize(22);
  doc.text("FICHE PATIENT", 20, 20);

  doc.setDrawColor(0, 0, 0);
  doc.line(20, 25, 190, 25); // Ligne de séparation

  // 3. Infos Générales
  doc.setFont("helvetica", "normal");
  doc.setFontSize(12);
  doc.text(`Nom complet : ${p.patient || 'N/A'}`, 20, 40);
  doc.text(`Âge : ${p.age || 'N/A'} ans`, 20, 50);
  doc.text(`Sexe : ${p.sexe || 'N/A'}`, 20, 60);
  doc.text(`Profession : ${p.profession || 'N/A'}`, 20, 70);

  // 4. Comorbidités
  doc.setFont("helvetica", "bold");
  doc.text("Comorbidités :", 20, 90);
  doc.setFont("helvetica", "normal");

  let y = 100;
  if (Array.isArray(detail.comorbidites) && detail.comorbidites.length > 0) {
    detail.comorbidites.forEach((c: any) => {
      const date = c.date_diagnostic ? new Date(c.date_diagnostic).toLocaleDateString() : 'Date inconnue';
      doc.text(`• ${c.libelle || 'Inconnu'} (${c.categorie || 'N/A'}) - Diagnostiqué le : ${date}`, 25, y);
      y += 8;
    });
  } else {
    doc.text("Aucune comorbidité enregistrée.", 25, y);
    y += 8;
  }

  // 5. Dernier suivi
  y += 10;
  doc.setFont("helvetica", "bold");
  doc.text(`Dernier suivi (${s.date_suivi ? new Date(s.date_suivi).toLocaleDateString() : 'N/A'}) :`, 20, y);

  doc.setFont("helvetica", "normal");
  y += 8;
  doc.text(`Poids : ${s.poids || '0'} kg  |  IMC : ${s.imc || 'N/A'}`, 20, y);
  y += 8;
  doc.text(`Tension : ${s.tension_systolique || '--'}/${s.tension_diastolique || '--'} mmHg`, 20, y);
  y += 10;
  doc.text(`Notes : ${s.notes_evolution || 'Aucune note.'}`, 20, y, { maxWidth: 170 });

  // 6. Téléchargement
  doc.save(`fiche_patient_${p.id_patient || 'inconnu'}.pdf`);
}



  toggleNuit(idNuit: number) {
    this.nuitOuverte.set(this.nuitOuverte() === idNuit ? null : idNuit);
  }
  iahLabel(iah: number | null): string {
    if (iah === null || iah === undefined) return 'N/A';
    if (iah < 5) return `Normal (${iah.toFixed(1)})`;
    if (iah < 15) return `Léger (${iah.toFixed(1)})`;
    if (iah < 30) return `Modéré (${iah.toFixed(1)})`;
    return `⚠ Sévère (${iah.toFixed(1)})`;
  }

  iahClasse(iah: number | null): string {
    if (iah === null || iah === undefined) return 'pill-blue';
    if (iah < 5) return 'pill-green';
    if (iah < 15) return 'pill-amber';
    return 'pill-red';
  }
}
