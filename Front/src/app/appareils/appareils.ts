import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth';
import { SidebarComponent } from '../components/sidebar/sidebar';
@Component({
  selector: 'app-appareils',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  templateUrl: './appareils.html',
  styleUrl: './appareils.css',
})
export class Appareils implements OnInit {
  private authService = inject(AuthService);
  appareils = this.authService.appareils;

  ngOnInit() {
    this.authService.getAppareils().subscribe();
  }
}
