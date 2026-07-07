import { Component, inject, OnInit } from '@angular/core';
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

  nuits = this.authService.nuits;

  ngOnInit() {
    this.authService.fetchNuits().subscribe({
      next: () => console.log('Nuits chargées'),
      error: (err: any) => console.error('Erreur API:', err),
    });
  }
}
