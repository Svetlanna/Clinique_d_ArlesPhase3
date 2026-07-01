import { Component, computed, inject, signal } from '@angular/core';
import { AuthService } from '../services/auth';
import { SidebarComponent } from '../components/sidebar/sidebar';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [SidebarComponent],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard {
  protected readonly title = signal('CliniquePlus');

  private authService = inject(AuthService);

  user = this.authService.currentUser;

  protected showMedecin = computed(() => {
    const role = this.user()?.role;
    return role === 'admin' || role === 'medecin';
  });

  protected showOperateur = computed(() => {
    const role = this.user()?.role;
    return role === 'admin' || role === 'operateur';
  });
}
