import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from '../components/sidebar/sidebar';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-test-operateur',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './test-operateur.html',
  styleUrl: './test-operateur.css',
})
export class TestOperateur {
  private authService = inject(AuthService);
  user = this.authService.currentUser;
}
