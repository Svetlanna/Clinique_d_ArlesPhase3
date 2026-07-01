import { Injectable, signal } from '@angular/core';
import {Router} from "@angular/router"


const TOKEN_KEY = 'auth_token';

@Injectable({ providedIn: 'root' })
export class LocalService {
    constructor(private router: Router) { }

    estConnecte = signal<boolean>(localStorage.getItem(TOKEN_KEY) !== null);

    login(token: string) {
        localStorage.setItem(TOKEN_KEY, token);
        this.estConnecte.set(true);
    }

    logout() {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem('auth_role');
        this.estConnecte.set(false);
        this.router.navigate(['/'])
    }

    saveToken(key: string, value: string) {
        localStorage.setItem(key, value);
    }

    getToken(key: string) {
        return localStorage.getItem(key);
    }

    removeToken(key: string) {
        localStorage.removeItem(key);
    }
}
