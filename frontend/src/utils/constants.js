export const JOB_STATUSES = {
  DRAFT: 'draft',
  ACTIVE: 'active',
  CLOSED: 'closed',
};

export const JOB_STATUS_LABELS = {
  [JOB_STATUSES.DRAFT]: 'Draft',
  [JOB_STATUSES.ACTIVE]: 'Active',
  [JOB_STATUSES.CLOSED]: 'Closed',
};

export const JOB_STATUS_COLORS = {
  [JOB_STATUSES.DRAFT]: 'default',
  [JOB_STATUSES.ACTIVE]: 'success',
  [JOB_STATUSES.CLOSED]: 'error',
};

export const CRITERIA_AREAS = [
  'Personal Information',
  'Address Information',
  'Education',
  'Professional Experience',
  'Years of Experience',
  'Computer Proficiency',
  'Public Sector Employment',
  'Language Proficiency',
  'Additional Skills',
  'Other Information',
  'Certification Statement',
];

export const DEFAULT_MAX_SCORES = {
  'Education': 15,
  'Professional Experience': 25,
  'Computer Proficiency': 10,
  'Language Proficiency': 10,
  'Additional Skills': 15,
  'Other': 25,
};