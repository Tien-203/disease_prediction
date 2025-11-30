/**
 * Routes Configuration
 * Centralized route paths to avoid hardcoding
 */

export interface NavLink {
  label: string;
  path: string;
  exact?: boolean;
  icon?: string;
}

export const ROUTE_PATHS = {
  // Auth routes
  LOGIN: '/login',
  REGISTER: '/register',

  // Patient routes
  PATIENT: {
    HOME: '/patient',
    PROFILE: '/profile',
    HISTORY: '/history',
    PREDICTION: '/prediction'
  },

  // Doctor routes
  DOCTOR: {
    HOME: '/doctor',
    DASHBOARD: '/doctor/dashboard',
    PROFILE: '/doctor/profile',
    DATASET: '/doctor/dataset',
    PATIENTS: '/doctor/patients'
  },

  // Data Scientist routes
  DATA_SCIENTIST: {
    HOME: '/data-scientist/dashboard',
    DASHBOARD: '/data-scientist/dashboard',
    PROFILE: '/data-scientist/profile',
    DATASET: '/data-scientist/dataset'
  },

  // Researcher routes
  RESEARCHER: {
    HOME: '/researcher',
    DASHBOARD: '/researcher/dashboard',
    PROFILE: '/researcher/profile',
    DATASET: '/researcher/dataset',
    PATIENTS: '/researcher/patients'
  }
} as const;

/**
 * Navigation links for each role
 */
export const ROLE_NAV_LINKS: Record<string, NavLink[]> = {
  patient: [
    { label: 'Home', path: ROUTE_PATHS.PATIENT.HOME },
    { label: 'Profile', path: ROUTE_PATHS.PATIENT.PROFILE },
    { label: 'History', path: ROUTE_PATHS.PATIENT.HISTORY }
  ],

  doctor: [
    { label: 'Profile', path: ROUTE_PATHS.DOCTOR.PROFILE },
    { label: 'Dataset', path: ROUTE_PATHS.DOCTOR.DATASET },
    { label: 'Patient Log', path: ROUTE_PATHS.DOCTOR.PATIENTS }
  ],

  data_scientist: [
    { label: 'Home', path: ROUTE_PATHS.DATA_SCIENTIST.HOME },
    { label: 'Profile', path: ROUTE_PATHS.DATA_SCIENTIST.PROFILE },
    { label: 'Dataset', path: ROUTE_PATHS.DATA_SCIENTIST.DATASET }
  ],

  datascientist: [
    { label: 'Home', path: ROUTE_PATHS.DATA_SCIENTIST.HOME },
    { label: 'Profile', path: ROUTE_PATHS.DATA_SCIENTIST.PROFILE },
    { label: 'Dataset', path: ROUTE_PATHS.DATA_SCIENTIST.DATASET }
  ],

  researcher: [
    { label: 'Profile', path: ROUTE_PATHS.RESEARCHER.PROFILE },
    { label: 'Dataset', path: ROUTE_PATHS.RESEARCHER.DATASET },
    { label: 'Patient Log', path: ROUTE_PATHS.RESEARCHER.PATIENTS }
  ]
};

/**
 * Routes where header/footer should be hidden
 */
export const HIDE_LAYOUT_ROUTES = [
  ROUTE_PATHS.LOGIN,
  ROUTE_PATHS.REGISTER
];

/**
 * Get home route for a specific role
 */
export function getHomeRouteForRole(role?: string | null): string {
  const normalizedRole = role?.toLowerCase().replace(/\s+/g, '_');

  switch (normalizedRole) {
    case 'data_scientist':
    case 'datascientist':
      return ROUTE_PATHS.DATA_SCIENTIST.HOME;
    case 'doctor':
      return ROUTE_PATHS.DOCTOR.HOME;
    case 'researcher':
      return ROUTE_PATHS.RESEARCHER.HOME;
    case 'patient':
    default:
      return ROUTE_PATHS.PATIENT.HOME;
  }
}
