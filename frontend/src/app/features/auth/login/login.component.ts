import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink, NavigationEnd } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { Subscription, filter } from 'rxjs';
import { NzAlertModule } from 'ng-zorro-antd/alert';

/**
 * Login Component - Refactored with Bootstrap 5 and ng-zorro
 */
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, NzAlertModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  email: string = '';
  password: string = '';
  selectedRole: 'patient' | 'doctor' | 'researcher' | 'data_scientist' = 'patient';
  loading: boolean = false;
  error: string | null = null;
  readonly roles = [
    { value: 'patient', label: 'Patient' },
    { value: 'doctor', label: 'Doctor' },
    { value: 'researcher', label: 'Researcher' },
    { value: 'data_scientist', label: 'Data Scientist' }
  ];

  private routerSubscription?: Subscription;

  constructor(
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    // Check if already authenticated and redirect after component is fully initialized
    if (this.authService.isAuthenticated()) {
      const currentUser = this.authService.getCurrentUser();
      // Use setTimeout to ensure component is fully initialized before navigation
      setTimeout(() => {
        this.redirectToRole(currentUser?.role);
      }, 0);
    }

    // Reset loading state if navigation occurs
    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        console.log('Navigation detected, resetting loading state');
        this.loading = false;
        this.error = null;
      });
  }

  ngOnDestroy(): void {
    console.log('LoginComponent ngOnDestroy called - component is being destroyed');
    this.routerSubscription?.unsubscribe();
    // Ensure loading state is reset when component is destroyed
    this.loading = false;
  }

  /**
   * Handle form submission
   */
  onSubmit() {
    if (!this.email || !this.password) {
      this.error = 'Please enter both email and password';
      return;
    }

    this.loading = true;
    this.error = null;

    console.log('Login attempt:', { email: this.email, role: this.selectedRole });

    this.authService.login(this.email, this.password, this.selectedRole).subscribe({
      next: (response) => {
        console.log('Login component - next callback:', response);
        const roleFromResponse = response?.user?.role as typeof this.selectedRole | undefined;
        console.log('Redirecting with role:', roleFromResponse || this.selectedRole);
        
        // Navigate first, then reset loading state
        this.redirectToRole(roleFromResponse || this.selectedRole);
        
        // Reset loading state after navigation is initiated
        // Use setTimeout to ensure navigation happens first
        setTimeout(() => {
          this.loading = false;
          this.error = null;
        }, 100);
      },
      error: (err) => {
        console.error('Login component - error callback:', err);
        this.loading = false;
        this.error = err.message || 'Login failed. Please check your credentials.';
        this.cdr.detectChanges();
      },
      complete: () => {
        console.log('Login observable completed');
        // Ensure loading is false
        if (this.loading) {
          this.loading = false;
          this.cdr.detectChanges();
        }
      }
    });
  }

  private redirectToRole(role?: string | null) {
    const normalizedRole = role?.toLowerCase();
    console.log('redirectToRole called with:', normalizedRole);
    
    let targetRoute: string[] = ['/patient'];
    switch (normalizedRole) {
      case 'data_scientist':
        targetRoute = ['/ds'];
        break;
      case 'doctor':
        targetRoute = ['/doctor'];
        break;
      case 'researcher':
        targetRoute = ['/researcher'];
        break;
      default:
        targetRoute = ['/patient'];
        break;
    }
    
    console.log('Navigating to:', targetRoute);
    
    // Use router.navigate with proper error handling
    // Ensure navigation happens asynchronously to avoid blocking
    Promise.resolve().then(() => {
      this.router.navigate(targetRoute, { 
        replaceUrl: false,
        skipLocationChange: false
      }).then(success => {
        if (success) {
          console.log('Navigation successful to:', targetRoute);
        } else {
          console.warn('Navigation returned false for:', targetRoute);
        }
      }).catch(error => {
        console.error('Navigation error:', error);
      });
    });
  }
}

