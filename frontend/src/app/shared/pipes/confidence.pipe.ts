import { Pipe, PipeTransform } from '@angular/core';

/**
 * Pipe to format confidence as percentage
 */
@Pipe({
  name: 'confidence',
  standalone: true
})
export class ConfidencePipe implements PipeTransform {
  transform(value: number): string {
    if (value === null || value === undefined || isNaN(value)) {
      return '0%';
    }
    return `${(value * 100).toFixed(1)}%`;
  }
}
