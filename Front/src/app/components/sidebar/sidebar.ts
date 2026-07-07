import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.css',
})
export class SidebarComponent {
  private authService = inject(AuthService);
  protected readonly title = signal('CliniquePlus');

  // Apps Streamlit connectées directement à la base analytique (galaxie SQLite / MySQL).
  protected readonly urlResultatsNuitIA = 'http://localhost:8502';
  protected readonly urlDashboardCpap = 'http://localhost:8501';

  user = this.authService.currentUser;

  protected showMedecin = computed(() => {
    const role = this.user()?.role;
    return role === 'admin' || role === 'medecin';
  });

  protected showOperateur = computed(() => {
    const role = this.user()?.role;
    return role === 'admin' || role === 'operateur';
  });

  logout() {
    this.authService.logout();
  }
}
