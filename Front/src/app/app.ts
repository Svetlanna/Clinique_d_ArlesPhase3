import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
<<<<<<< HEAD

=======
import { Authification } from './authification/authification';
import { AuthService } from './services/auth';
>>>>>>> sophian
@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('CliniquePlus');
}
