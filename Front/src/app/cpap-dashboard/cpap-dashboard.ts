import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-cpap-dashboard',
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './cpap-dashboard.html',
  styleUrl: './cpap-dashboard.css',
})
export class CpapDashboard implements OnInit {
  private authService = inject(AuthService);
  cpap = this.authService.cpap;

  ngOnInit() {
    this.authService.fetchCpap().subscribe({
      next: () => console.log('Cpap chargés'),
      error: (err: any) => console.error('Erreur API:', err),
    });
  }
}
