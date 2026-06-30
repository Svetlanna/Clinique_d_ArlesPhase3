import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  templateUrl: './admin.html',
  styleUrls: ['./admin.css'],
})
export class AdminComponent implements OnInit {
  nuits: any[] = [];
  medecins: any[] = [];

  // Ces propriétés sont indispensables pour votre HTML
  showModal = false;
  selectedNuit: any = null;
  editForm = {
    commentaire: '',
    idMedecin: '',
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.chargerNuits();
    this.chargerMedecins();
  }

  chargerNuits() {
    this.http
      .get<any>('http://localhost:3000/api/nuits')
      .subscribe((res) => (this.nuits = res.data));
  }

  chargerMedecins() {
    this.http
      .get<any>('http://localhost:3000/api/med')
      .subscribe((res) => (this.medecins = res.data));
  }

  // C'est cette méthode que le HTML cherche à appeler
  openEditModal(nuit: any) {
    this.selectedNuit = nuit;
    this.editForm = {
      commentaire: nuit.notes_techniques || '',
      idMedecin: nuit.id_medecin || '',
    };
    this.showModal = true;
  }

  saveChanges() {
    if (!this.selectedNuit) return;

    this.http
      .put(`http://localhost:3000/api/nuits/${this.selectedNuit.id}/update`, this.editForm)
      .subscribe(() => {
        this.chargerNuits();
        this.showModal = false;
      });
  }
}
