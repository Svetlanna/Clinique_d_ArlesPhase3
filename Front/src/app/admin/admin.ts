import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { AuthService } from '../../app/services/auth';
import { Router } from '@angular/router';
@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css'],
})
export class AdminComponent implements OnInit {
  private router = inject(Router);
  private http = inject(HttpClient);
  private authService = inject(AuthService);

  // BUG FIX : l'app tourne en zoneless (pas de zone.js dans package.json /
  // angular.json => Angular 22 zoneless par défaut). Dans ce mode, muter une
  // simple propriété de classe (nuits: any[] = []) DANS un callback
  // .subscribe() ne déclenche PAS de rafraîchissement de la vue : les
  // données arrivent bien en mémoire, mais l'écran ne se met à jour que si
  // un autre événement (ex: un clic qui déclenche une navigation) force une
  // détection de changement au passage. D'où le "ça marche au 2e clic".
  // On passe donc nuits/medecins en signals, comme le fait déjà
  // nuits-patients.ts (qui lui n'a jamais eu ce problème).
  nuits = signal<any[]>([]);
  medecins = signal<any[]>([]);

  user = this.authService.currentUser;
  userRole = computed(() => this.user()?.role);

  showModal = false;
  selectedNuit: any = null;
  editForm = {
    commentaire: '',
    idMedecin: '',
  };

  constructor() {}

  ngOnInit() {
    this.chargerNuits();
    this.chargerMedecins();
  }

  chargerNuits() {
    this.http.get<any>('http://localhost:3000/api/nuit').subscribe((res) => {
      console.log('Contenu de la réponse API :', res);
      this.nuits.set(res.data || res);
    });
  }

  chargerMedecins() {
    this.http.get<any>('http://localhost:3000/api/med').subscribe((res) => {
      this.medecins.set(res.data);
    });
  }

  openEditModal(nuit: any) {
    this.selectedNuit = nuit;
    this.editForm = {
      commentaire: nuit.commentaire_medical || '',
      idMedecin: '',
    };
    this.showModal = true;
  }

  saveChanges() {
    const idNuit = this.selectedNuit?.id_nuit;

    const requetes = [];

    requetes.push(
      this.http.patch(`http://localhost:3000/api/nuit/${idNuit}/commentaire`, {
        commentaire: this.editForm.commentaire,
      }),
    );

    if (this.editForm.idMedecin) {
      requetes.push(
        this.http.patch(`http://localhost:3000/api/nuit/${idNuit}/medecin`, {
          idMedecin: this.editForm.idMedecin,
        }),
      );
    }

    let restantes = requetes.length;
    requetes.forEach((req) =>
      req.subscribe({
        next: () => {
          restantes--;
          if (restantes === 0) {
            this.chargerNuits();
            this.showModal = false;
          }
        },
        error: (err) => console.error('Erreur lors de la mise à jour:', err),
      }),
    );
  }
}
