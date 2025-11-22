import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

/**
 * Loading service to manage loading state
 */
@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();

  /**
   * Show loading indicator
   */
  show(): void {
    this.loadingSubject.next(true);
  }

  /**
   * Hide loading indicator
   */
  hide(): void {
    this.loadingSubject.next(false);
  }

  /**
   * Get current loading state
   */
  isLoading(): boolean {
    return this.loadingSubject.value;
  }
}


