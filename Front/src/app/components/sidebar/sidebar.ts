import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent {
  // Injections
  private authService = inject(AuthService);
  private router = inject(Router);

  // Attributs
  protected readonly title = signal('CliniquePlus');
  user = this.authService.currentUser;

  // Fonctions
  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
