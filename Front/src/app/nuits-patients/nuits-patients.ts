import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth';
import { SidebarComponent } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-nuits-patients',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './nuits-patients.html',
  styleUrl: './nuits-patients.css',
})
export class NuitsPatients implements OnInit {
  private authService = inject(AuthService);

  medecines = this.authService.medecines;
  nuits = this.authService.nuits;
  commentaire = signal('')
  identifier = signal(0)

  enregistrer(){
    this.authService.updateCommentaire(this.identifier(),this.commentaire()).subscribe({
      next: () => console.log('commentaire enregistré'),
      error: (err) => console.error('Erreur API:', err),
    })
  }
  



  ngOnInit() {
    this.authService.fetchMedecines().subscribe({
      next: (res) => console.log('Médecins chargés:', res),
      error: (err) => console.error('Erreur API:', err),
    });

    this.authService.fetchNuits().subscribe({
      next: () => console.log('Nuits chargées'),
      error: (err) => console.error('Erreur API:', err),
    });
  }
}