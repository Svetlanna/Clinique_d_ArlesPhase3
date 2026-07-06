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
  private getPatientSlug(nom: string): string {
    return nom
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Enlève les accents
      .replace(/\s+/g, '_'); // Remplace les espaces par des _
  }

  getCheminCourbe(type: string, numero: number): string {
    const nom = this.patientDetail()?.patient.patient || 'inconnu';
    return `/courbe_${type}_nuit_${numero}.png`;
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

  private loadImage(url: string): Promise<HTMLImageElement> {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'Anonymous';
      img.onload = () => resolve(img);
      img.onerror = (err) => reject(err);
      img.src = url;
    });
  }
  async genererFichierPatientPDF() {
    const detail = this.patientDetail();
    if (!detail || !detail.patient || !detail.dernierSuivi) {
      alert('Données patient indisponibles.');
      return;
    }

    const doc = new jsPDF();
    const p = detail.patient;
    const s = detail.dernierSuivi;
    let y = 20; // Point de départ

    // 1. En-tête
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.text('FICHE PATIENT', 20, y);
    y += 5;
    doc.line(20, y, 190, y);
    y += 15;

    // 2. Infos Générales
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    doc.text(`Nom complet : ${p.patient || 'N/A'}`, 20, y);
    y += 10;
    doc.text(`Âge : ${p.age || 'N/A'} ans`, 20, y);
    y += 10;
    doc.text(`Sexe : ${p.sexe || 'N/A'}`, 20, y);
    y += 10;
    doc.text(`Profession : ${p.profession || 'N/A'}`, 20, y);
    y += 15;

    // 3. Comorbidités
    doc.setFont('helvetica', 'bold');
    doc.text('Comorbidités :', 20, y);
    y += 8;
    doc.setFont('helvetica', 'normal');
    if (Array.isArray(detail.comorbidites) && detail.comorbidites.length > 0) {
      detail.comorbidites.forEach((c: any) => {
        const date = c.date_diagnostic
          ? new Date(c.date_diagnostic).toLocaleDateString()
          : 'Date inconnue';
        doc.text(`• ${c.libelle} (${c.categorie}) - Diagnostiqué le : ${date}`, 25, y);
        y += 8;
      });
    } else {
      doc.text('Aucune comorbidité.', 25, y);
      y += 8;
    }

    // 4. Dernier suivi
    y += 10;
    doc.setFont('helvetica', 'bold');
    doc.text(
      `Dernier suivi (${s.date_suivi ? new Date(s.date_suivi).toLocaleDateString() : 'N/A'}) :`,
      20,
      y,
    );
    y += 8;
    doc.setFont('helvetica', 'normal');
    doc.text(`Poids : ${s.poids || '0'} kg | IMC : ${s.imc || 'N/A'}`, 20, y);
    y += 8;
    doc.text(`Notes : ${s.notes_evolution || 'Aucune note.'}`, 20, y, { maxWidth: 170 });
    y += 20; // Espace avant la courbe

    // 5. Ajout de l'image (Courbe)
    try {
      const imgUrl = this.getCheminCourbe('debit_nasal', 1);
      const imgData = await this.loadImage(imgUrl);

      // Si la courbe dépasse la page, on en crée une nouvelle
      if (y > 200) {
        doc.addPage();
        y = 20;
      }

      doc.setFont('helvetica', 'bold');
      doc.text('Courbe de débit nasal :', 20, y);
      doc.addImage(imgData, 'PNG', 20, y + 5, 170, 80);
    } catch (e) {
      console.error('Erreur chargement image');
    }

    doc.save(`fiche_patient_${p.id_patient}.pdf`);
  }
}
