import { Component, OnInit, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { AuthService } from '../../app/services/auth';
import { Router, NavigationEnd } from '@angular/router';
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
  nuits: any[] = [];
  medecins: any[] = [];

  user = this.authService.currentUser;
  userRole = computed(() => this.user()?.role);

  showModal = false;
  selectedNuit: any = null;
  editForm = {
    commentaire: '',
    idMedecin: '',
  };


  constructor() {
    this.router.events.subscribe((event) => {
     // if (event instanceof NavigationEnd) {
        this.chargerNuits();
        this.chargerMedecins();
      //}
    });
  }

  ngOnInit() {
    this.chargerNuits();
    this.chargerMedecins();
  }

  chargerNuits() {
    this.http.get<any>('http://localhost:3000/api/nuit').subscribe((res) => {
      console.log('Contenu de la réponse API :', res); // Regardez ici dans la console
      this.nuits = res.data || res; // S'adapte si la structure change
    });
  }

  chargerMedecins() {
    this.http.get<any>('http://localhost:3000/api/med').subscribe((res) => {
      this.medecins = res.data;
    });
  }

  openEditModal(nuit: any) {
    this.selectedNuit = nuit;
    this.editForm = {
      commentaire: nuit.notes_techniques || '',
      idMedecin: nuit.id_medecin || '',
    };
    this.showModal = true;
  }

  saveChanges() {
    const idNuit = this.selectedNuit?.id_nuit;

    const payload = {
      commentaire: this.editForm.commentaire,
      idMedecin: this.editForm.idMedecin,
    };

    this.http.put(`http://localhost:3000/api/nuit/${idNuit}/update`, payload).subscribe({
      next: () => {
        this.chargerNuits();
        this.showModal = false;
      },
      error: (err) => console.error('Erreur lors de la mise à jour:', err),
    });
  }
}
