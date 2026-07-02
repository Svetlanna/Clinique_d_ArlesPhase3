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
  commentaire = signal('');
  identifier = signal(0);
  popUp = signal(false);

  ngOnInit() {
    this.authService.fetchMedecines().subscribe({
      next: () => console.log('Médecins chargés'),
      error: (err: any) => console.error('Erreur API:', err),
    });
    this.authService.fetchNuits().subscribe({
      next: () => console.log('Nuits chargées'),
      error: (err: any) => console.error('Erreur API:', err),
    });
  }

  enregistrer() {
    this.authService.updateCommentaire(this.identifier(), this.commentaire()).subscribe({
      next: () => (
        this.popUp.set(true),
        console.log('Commentaire enregistré'),
        setTimeout(() => {
          this.popUp.set(false);
        }, 3000)
      ),
      error: (err: any) => console.error('Erreur:', err),
    });
  }
}
