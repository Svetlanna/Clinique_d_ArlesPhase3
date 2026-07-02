import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Authification } from './authification/authification';
import { AuthService } from './services/auth';
@Component({
  selector: 'app-root',
  imports: [Authification,RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('CliniquePlus');
}
