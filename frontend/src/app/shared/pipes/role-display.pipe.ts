import { Pipe, PipeTransform } from '@angular/core';
import { UserRole } from '../../core/models/user.model';

/**
 * Pipe to format role names for display
 */
@Pipe({
  name: 'roleDisplay',
  standalone: true
})
export class RoleDisplayPipe implements PipeTransform {
  transform(role: UserRole | string): string {
    const roleMap: { [key: string]: string } = {
      'patient': 'Patient',
      'doctor': 'Doctor',
      'researcher': 'Researcher',
      'data_scientist': 'Data Scientist'
    };
    
    return roleMap[role] || role;
  }
}
